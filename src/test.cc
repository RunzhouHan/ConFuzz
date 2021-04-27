#include <fstream>
#include <iostream>
#include <math.h>
#include <set>
#include <cstdlib>
#include <ctime>
#include <sys/stat.h>
#include <unordered_map>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include "ext2fs/ext2_fs.h"
#include "ext2fs/ext2fs.h"

using std::cout;
using std::endl;
using std::unordered_map;
using std::fstream;
using std::ios;
using std::string;

#define LOG(err) if (err != 0) cout << err << endl;

#define LEVEL_ZERO_MUTATION 0
#define LEVEL_ONE_MUTATION 1
#define LEVEL_TWO_MUTATION 2

struct offset_length
{
    long long int offset;
    unsigned int length; 
};

/* type-aware metadata hash table. */
unordered_map <long long unsigned int, struct offset_length> meta_dict;

/* level zero corruption parameters */
unsigned long long int user_corrupt_bytes = 0;
double user_corrupt_pct = 0.0;

/* number of total fields */
long long int field_count = 0;

enum level_one_structures {
  _superblock,            
  _bgd,                   
  _GDT,                   
  _meta_bg,               
  _block_bitmap,          
  _inode_bitmap,          
  _inode_table,           
  // extended_attribute,  
  // MMP,                 
  kNum
};

typedef unordered_map <int, std::string> num_2_name_map;
num_2_name_map level_one_structure_dict ( {
    {_superblock, "superblock"}, 
    {_bgd, "bgd"}, {_GDT, "GDT"}, 
    {_meta_bg, "meta_bg"}, 
    {_block_bitmap, "block bitmap"}, 
    {_inode_bitmap, "inode bitmap"}, 
    {_inode_table, "inode table"}
  } );

/* structure bitmap to decide which fields to be fuzzed */
char* structure_bitmap;

void init_structure_bitmap() {
  long long int bitmap_len = ceil(field_count / 8);
  structure_bitmap = new char[bitmap_len];
}

/* misc */
int random(int from, int to){
  return rand() % (to - from + 1) + from;
}

void int32_2_char(int b, char b_[4]) {
  b_[0] = (b >> 24) & 0xFF;
  b_[1] = (b >> 16) & 0xFF;
  b_[2] = (b >> 8) & 0xFF;
  b_[3] = b & 0xFF;
}

int find_super_and_bgd(ext2_filsys fs, dgrp_t group)
{
  blk64_t super_blk, old_desc_blk, new_desc_blk;
  blk_t used_blks;
  int old_desc_blocks, num_blocks;

  ext2fs_super_and_bgd_loc2(fs, group, &super_blk,
          &old_desc_blk, &new_desc_blk, &used_blks);

  if (EXT2_HAS_INCOMPAT_FEATURE(fs->super, EXT2_FEATURE_INCOMPAT_META_BG))
    old_desc_blocks = fs->super->s_first_meta_bg;
  else
    old_desc_blocks = fs->desc_blocks + fs->super->s_reserved_gdt_blocks;
  
  if (super_blk || (group == 0))
    // ext2fs_mark_block_bitmap2(bmap, super_blk);
    meta_dict[_superblock + group * kNum] = {super_blk * fs->blocksize, fs->blocksize}; 

  if ((group == 0) && (fs->blocksize == 1024) &&
      EXT2FS_CLUSTER_RATIO(fs) > 1)
    // ext2fs_mark_block_bitmap2(bmap, 0);
    meta_dict[_superblock + group * kNum] = {0,fs->blocksize}; 

  if (super_blk == 0)
    meta_dict[_superblock + group * kNum] = {-1,fs->blocksize}; 

  // cout << "superblock offset and size for group " << group << " are " \
    << meta_dict[_superblock + group * kNum].offset << ", " \
    << meta_dict[_superblock + group * kNum].length << endl;
  
  if (old_desc_blk) {
    num_blocks = old_desc_blocks;
    if (old_desc_blk + num_blocks >= ext2fs_blocks_count(fs->super))
        num_blocks = ext2fs_blocks_count(fs->super) - old_desc_blk;
    // ext2fs_mark_block_bitmap_range2(bmap, old_desc_blk, num_blocks);
    // for (blk64_t i = old_desc_blk; i < old_desc_blk + std::min(num_blocks, int(2)); i++)
    meta_dict[_bgd + group * kNum] = {old_desc_blk * fs->blocksize, EXT2_DESC_SIZE(fs->super)};
    meta_dict[_GDT + group * kNum] = {(old_desc_blk + 1) * fs->blocksize, num_blocks * fs->blocksize};
  }
  else {
    meta_dict[_bgd + group * kNum] = {-1, EXT2_DESC_SIZE(fs->super)};
    meta_dict[_GDT + group * kNum] = {-1, EXT2_DESC_SIZE(fs->super)};
  }

  // cout << "bgd offset and size for group " << group << " are " \
    << meta_dict[_bgd + group * kNum].offset << ", " \
    << meta_dict[_bgd + group * kNum].length << endl;
  // cout << "reserved GDT offset and size for group " << group << " are " \
    << meta_dict[_GDT + group * kNum].offset << ", " \
    << meta_dict[_GDT + group * kNum].length << endl;

  if (new_desc_blk)
    meta_dict[_meta_bg + group * kNum] = {new_desc_blk * fs->blocksize, EXT2_DESC_PER_BLOCK(fs->super) * EXT2_DESC_SIZE(fs->super)};
  else 
    meta_dict[_meta_bg + group * kNum] = {-1, EXT2_DESC_PER_BLOCK(fs->super) * EXT2_DESC_SIZE(fs->super)};
  
  // cout << "meta_bg offset and size for group " << group << " are " \
    << meta_dict[_meta_bg + group * kNum].offset << ", " \
    << meta_dict[_meta_bg + group * kNum].length << endl;

  return 0;
}

errcode_t find_metadata_blocks(ext2_filsys fs)
{
  blk64_t b, c;
  ext2_inode_scan scan;
  ext2_ino_t ino;
  struct ext2_inode inode;
  errcode_t retval;
  dgrp_t group_count = fs->group_desc_count;

  for (dgrp_t i = 0; i < group_count; i++) {
    find_super_and_bgd(fs, i);

    b = ext2fs_block_bitmap_loc(fs, i);
    meta_dict[_block_bitmap + i * kNum] = {b * fs->blocksize, fs->blocksize};
    // cout << "block bitmap block of group " << i << " starts at " \
      << meta_dict[_block_bitmap + i * kNum].offset << endl;
    
    b = ext2fs_inode_bitmap_loc(fs, i);
    meta_dict[_inode_bitmap + i * kNum] = {b * fs->blocksize, fs->blocksize};
    // cout << "inode bitmap block of group " << i << " starts at " \
      << meta_dict[_inode_bitmap + i * kNum].offset << endl;
    
    c = ext2fs_inode_table_loc(fs, i);
    meta_dict[_block_bitmap + i * kNum] = {c * fs->blocksize, fs->blocksize * fs->inode_blocks_per_group};
    // cout << "inode bitmap block of group " << i << " starts at " \
      << meta_dict[_block_bitmap + i * kNum].offset << endl;    
    
    // cout << "\n" << endl;
  }

  return retval;
}

int level_one_structure_selector() {
  int structure_num;
  srand(time(NULL)); 
  structure_num = random(0,field_count);      // single level one structure selection
  return structure_num;
}

void level_one_image_mutation(const char *path) {
  fstream fs_file;
  int a, b, structure_num;
  offset_length offset;   //taba
  long long int location;  //taba
  char b_[4];
  bool not_exist = 1;

  fs_file.open(path, fstream::in | fstream::out | fstream::binary);

  while (not_exist) {
    structure_num = level_one_structure_selector();
    if (meta_dict[structure_num].offset >= 0) 
      not_exist = 0;
  }

  cout << "Corruption at key " << structure_num \
    << " : " << level_one_structure_dict[structure_num % kNum] \
    << " of group " << floor(structure_num / kNum) <<  " is selected" << endl;

  srand(time(NULL));  //taba
  a = random(0, meta_dict[structure_num].length-4);  //taba
  location = meta_dict[structure_num].offset + a;  //taba
  cout << "Corrupt " << sizeof(int) << " bytes starting from location "  \ 
    << location << " (in byte)" << endl;  //taba

  srand(time(NULL));   //taba
  b = random(0, 0x7FFFFFF);  //taba  
  cout << "Corruption Value is = " << b << endl;  //taba 
  int32_2_char(b, b_);
 
  fs_file.seekg(location, ios::beg);  //taba
  fs_file.write(b_, 4);  //taba
  fs_file.close();
}

int process_fs(const char *path, int mutation_level) {
  errcode_t ret;
  ext2_filsys fs = NULL;
  blk64_t bitmap;
  blk64_t super;
  dgrp_t group_count;
  unsigned int icount;

  /* open file system */
  LOG(ext2fs_open(path, EXT2_FLAG_64BITS, 0, 0, unix_io_manager, &fs));
  group_count = fs->group_desc_count;
  field_count = kNum * group_count;

  /* initialize structure bitmap */
  init_structure_bitmap();

  /* three-level mutation */
  switch(mutation_level) {
    case 1: 
      ret = find_metadata_blocks(fs);
      level_one_image_mutation(path);
      break;
  }

  delete fs;
  delete structure_bitmap;

  return 0;
}

int main(int argc, char* argv[]) {
  int mutation_level;
  errcode_t ret;
  const char *in_path = argv[1];

  mutation_level = 1;
  //string meta = argv[2];     //taba
  ret = process_fs(in_path, mutation_level);
  // for (auto x : meta_dict)  //taba
  //   cout << x.first << " " << x.second.offset << " " << x.second.length << endl;  //taba
  return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// #include "./utiltiy_arg_template.hh"

enum mke2fs {
  _mke2fs_b, _mke2fs_c, _mke2fs_E, _mke2fs_f, 
  _mke2fs_F, _mke2fs_g, _mke2fs_G, _mke2fs_i, 
  _mke2fs_I, _mke2fs_j, _mke2fs_J, _mke2fs_K, 
  _mke2fs_l, _mke2fs_L, _mke2fs_m, _mke2fs_M, 
  _mke2fs_n, _mke2fs_N, _mke2fs_o, _mke2fs_O, 
  _mke2fs_q, _mke2fs_r, _mke2fs_S, _mke2fs_t, 
  _mke2fs_T, _mke2fs_U, _mke2fs_v, _mke2fs_V, 
  kNum_mke2fs
};

typedef char arg_array;

arg_array** mke2fs_args, e2fsck_args, resize2fs_args, tune2fs_args;

void build_dict(char* utility) {
  if (!strcmp(utility, "mke2fs")) {
    mke2fs_args = malloc (sizeof(arg_array**) * kNum_mke2fs);
    mke2fs_args[_mke2fs_b] = "-b";
    mke2fs_args[_mke2fs_c] = "-c";
    mke2fs_args[_mke2fs_E] = "-E";
    mke2fs_args[_mke2fs_f] = "-f";
    mke2fs_args[_mke2fs_F] = "-F";
    mke2fs_args[_mke2fs_g] = "-g";
    mke2fs_args[_mke2fs_G] = "-G";
    mke2fs_args[_mke2fs_i] = "-i";
    mke2fs_args[_mke2fs_I] = "-I";
    mke2fs_args[_mke2fs_j] = "-j";
    mke2fs_args[_mke2fs_J] = "-J";
    mke2fs_args[_mke2fs_K] = "-K";
    mke2fs_args[_mke2fs_l] = "-l";
    mke2fs_args[_mke2fs_L] = "-L";
    mke2fs_args[_mke2fs_m] = "-m";
    mke2fs_args[_mke2fs_M] = "-M";
    mke2fs_args[_mke2fs_n] = "-n";
    mke2fs_args[_mke2fs_N] = "-N";
    mke2fs_args[_mke2fs_o] = "-o";
    mke2fs_args[_mke2fs_O] = "-O";
    mke2fs_args[_mke2fs_q] = "-q";
    mke2fs_args[_mke2fs_r] = "-r";
    mke2fs_args[_mke2fs_S] = "-S";
    mke2fs_args[_mke2fs_t] = "-t";
    mke2fs_args[_mke2fs_T] = "-T";
    mke2fs_args[_mke2fs_U] = "-U";
    mke2fs_args[_mke2fs_v] = "-v";
    mke2fs_args[_mke2fs_V] = "-V";
  }
}

void free_dicts() {
  // if (mke2fs_args )
  free(mke2fs_args);
}

/* predefined must-have arguments for each utility. 
   For instance, mke2fs must specify file system type with -t */
const int mke2fs_must_have[] = {_mke2fs_t};

typedef int arg_num;

/* input for afl */
typedef unsigned char arg_binary;

arg_binary* mke2fs_bin, e2fsck_bin, resize2fs_bin, tune2fs_bin;

arg_binary* binary_build_helper(char* utility) {
  int len;
  arg_binary* binary;

  if (!strcmp(utility, "mke2fs")) {
    len = 4 * sizeof(arg_binary*) * kNum_mke2fs; //
    mke2fs_bin = (arg_binary*) malloc (4 * sizeof(arg_binary*) * kNum_mke2fs); 
  }
  return binary;
  
}

void free_binary() {
  // if (mke2fs_args )
  free(mke2fs_bin);
}

char* arg_aggregator() {
  char* cmd;

  return cmd;
}

int main(int argc, char* argv[]) {
  int i, rc;
  int utility_count;
  char* cmd;

  char* utility[] = {"mke2fs"}; // to be replaced by argv[] or something else
  utility_count = 1; // to be replaced by argc or something else

  for (i = 0; i < utility_count; i++){
    build_dict(utility[i]);
    binary_build_helper(utility[i]);
  }

  cmd = arg_aggregator();

  printf("%s\n", mke2fs_bin);

  int must_have[] = {_mke2fs_T, _mke2fs_S, _mke2fs_t, _mke2fs_S, _mke2fs_t};

  free_dicts();
  // cout << _mke2fs_t << endl;
  // cout << tree->utility << tree->must_have << endl;
  // for(int i = 0; i != tree->must_have.size(); i++) {
  //   cout <<  tree->must_have[i] << endl;
  // }

  // delete tree;
  return 0;
}
#include <algorithm>
// #include <cstdlib>
#include <cstring>
// #include <ctime>
// #include <fstream>
#include <iostream>
// #include <math.h>
// #include <set>
// #include <sys/stat.h>
// #include <stdio.h>
// #include <stdlib.h>
#include <string>
// #include <unistd.h>  //getopt()
#include <unordered_map>
#include <utility>
#include <vector>

// #include "./utiltiy_arg_template.hh"

using std::cout;
using std::endl;
using std::unordered_map;
// using std::fstream;
// using std::ios;
using std::string;
// using std::pair;
using std::vector;


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

typedef unordered_map <int, std::string> arg_dictionary;

arg_dictionary mke2fs_args ( {
    {_mke2fs_b, "-b"}, 
    {_mke2fs_c, "-c"}, 
    {_mke2fs_E, "-E"}, 
    {_mke2fs_f, "-f"}, 
    {_mke2fs_F, "-F"}, 
    {_mke2fs_g, "-g"},
    {_mke2fs_G, "-G"}, 
    {_mke2fs_i, "-i"}, 
    {_mke2fs_I, "-I"},
    {_mke2fs_j, "-j"},
    {_mke2fs_J, "-J"},
    {_mke2fs_K, "-K"},
    {_mke2fs_l, "-l"},
    {_mke2fs_L, "-L"},
    {_mke2fs_m, "-m"},
    {_mke2fs_M, "-M"},
    {_mke2fs_n, "-n"},
    {_mke2fs_N, "-N"},
    {_mke2fs_o, "-o"},
    {_mke2fs_O, "-O"},
    {_mke2fs_q, "-q"},
    {_mke2fs_r, "-r"},
    {_mke2fs_S, "-S"},
    {_mke2fs_t, "-t"},
    {_mke2fs_T, "-T"},
    {_mke2fs_U, "-U"},
    {_mke2fs_v, "-v"},
    {_mke2fs_V, "V"}
  } );

/* predefined must-have arguments for each utility. 
   For instance, mke2fs must specify file system type with -t */
const int mke2fs_must_have[] = {_mke2fs_t};

typedef int arg_num;

/* input for afl */
typedef unsigned char arg_binary;

typedef struct arg_node {
  int num;
  string arg;
  bool enabled;
  arg_node* child_arg;
  string mutex;
  int v_type; // 0:int, 1:bool
  int index;
  int val;
}arg_node;

typedef struct root_node { 
  char* utility;
  vector<int> must_have;
  std::vector<arg_node*> child;
}root_node;


arg_binary* binary_build_helper(char* utility) {
  arg_binary* binary;

  if (!strcmp(utility, "mke2fs")) {
    arg_binary* binary = (arg_binary*) malloc (4 * sizeof(arg_binary) * kNum_mke2fs); 
  }
  
  return binary;
}

void insert_arg_node() {;}

// void insert_arg_node(root_node* tree, arg_num num) {
//   arg_node* node = new arg_node;

//   if (tree)
// }



void initialize_tree(root_node* tree, char* utility, int* must_have) {
  int i;
  tree->utility = utility;

  for (i = 0; i < sizeof(mke2fs_must_have)/sizeof(*mke2fs_must_have); i++) 
    tree->must_have.push_back(mke2fs_must_have[i]);

  if (!strcmp(tree->utility, "mke2fs")) {
      
      if (must_have) {
        for (i = 0; i < sizeof(must_have)/sizeof(*must_have); i++)
        tree->must_have.push_back(must_have[i]);
      }

      sort(tree->must_have.begin(), tree->must_have.end());
      tree->must_have.erase(unique(tree->must_have.begin(), tree->must_have.end()), tree->must_have.end());

      for (i = 0; i < kNum_mke2fs; i++)
        insert_arg_node();
  }

  else if (tree->utility == "badblocks") {
    ;
  }

  else if (tree->utility == "blkid") {
    ;
  }

  else if (tree->utility == "charttr") {
    ;
  }

  else if (tree->utility == "debugfs") {
    ;
  }

  else if (tree->utility == "dumpe2fs") {
    ;
  }

  else if (tree->utility == "e2freefrag") {
    ;
  }

  else if (tree->utility == "e2fsck") {
    ;
  }

  else if (tree->utility == "e2image") {
    ;
  }

  else if (tree->utility == "e2label") {
    ;
  }

  else if (tree->utility == "e2undo") {
    ;
  }

  else if (tree->utility == "e4defrag") {
    ;
  }

  else if (tree->utility == "filefrag") {
    ;
  }
  
  else if (tree->utility == "findfs") {
    ;
  }

  else if (tree->utility == "findsuper") {
    ;
  }

  else if (tree->utility == "logsave") {
    ;
  }

  else if (tree->utility == "lsattr") {
    ;
  }

  else if (tree->utility == "resize2fs") {
    ;
  }

  else if (tree->utility == "tune2fs") {
    ;
  }

  else 
    cout << "No such utility found!" << endl;
}

void initialize_arg_binary() {
  ;
}


string arg_aggregator() {
  string cmd;
  return cmd;
}


int main(int argc, char* argv[]) {
  int rc;
  char utility[] = "mke2fs"; 
  int must_have[] = {_mke2fs_T, _mke2fs_S, _mke2fs_t, _mke2fs_S, _mke2fs_t};
  // root_node* tree = new root_node;
  arg_binary* binary;
  // initialize_tree(tree, utility, must_have);
  binary = binary_build_helper(utility);

  // cout << _mke2fs_t << endl;
  // cout << tree->utility << tree->must_have << endl;
  // for(int i = 0; i != tree->must_have.size(); i++) {
  //   cout <<  tree->must_have[i] << endl;
  // }

  // delete tree;
  return 0;
}
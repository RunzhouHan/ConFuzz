#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <json.h>
#include <json_visit.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>
#include <math.h>

#include <sys/time.h>

#define EXIT_NORMALLY 0

/* fuzzing levels */
#define SEMANTICALLY_CORRECT 0 
#define SYNTACTICALLY_CORRECT 1 
#define SYNTACTICALLY_INCORRECT 2

/* buffer len */
#define MAX_CMD_LEN 1024
#define MAX_VAL_LEN 1024


/* input for afl */
typedef unsigned char bitmap;
typedef char** features;

typedef struct global_rules
{ 
  unsigned long fs_size;
  int** mutex_nodes;
/* Advanced fields may be added for special devices */
// #ifdef RAID
// #endif
// #ifdef SSD
// #endif
}global_rules;

typedef struct arg_node {
  char* arg;
  int value_type; 
  unsigned long* value_int;
  char* value_char;
  char** value_char_array;
  int char_array_len;
  char* operator_value;
  char* operator_sibling;
  char* operator_child;
  int* mutex;
  int mutex_len;
  bool must_have;
  int weight;
  bool must_child;
  int* child_id;
  int child_id_len;
  int* dependency_id;
  int dependency_id_len;
}arg_node;

typedef struct ir { 
  int enable;
  // int* bmap_index[2];
  unsigned long value_int;
  char* value_char;
}ir;

// void json_tree_parser(struct json_object* json_arg_tree, int* count);
int jso_count(json_object *jso, int flags, 
                                json_object *parent_jso, const char *jso_key, 
                                size_t *jso_index, int *count);
int json_tree_parse(struct json_object* json_arg_tree, arg_node* arg_array, 
                                                      int* arg_count) ;

int ct_builder(json_object *jso, int flags, 
                                json_object *parent_jso, const char *jso_key, 
                                size_t *jso_index, arg_node* arg_array);
int ct_display(arg_node* arg_array, int* len);
// int ct_free(arg_node* arg_array);

int bitmap_len(arg_node* arg_array, int* arg_count);
// int bitmap_init(arg_node* arg_array, int* arg_count, bitmap* arg_bitmap);
int bitmap_fuzz(bitmap* arg_bitmap, int* arg_count);
// int bitmap_free(bitmap* arg_bitmap);

int jso_count(json_object *jso, int flags, 
                                json_object *parent_jso, const char *jso_key, 
                                size_t *jso_index, int *count) {
  if (json_object_get_type(jso) == json_type_object)
      if (flags != JSON_C_VISIT_SECOND) 
        *count += 1;
  return JSON_C_VISIT_RETURN_CONTINUE;
}

int ct_display(arg_node* arg_array, int* len) {
  int i;
  for (i = 0; i < *len; i++) {
    printf("arg: %s id[%d]\n", arg_array[i].arg, i+1);
    printf("value_type: %d\n", arg_array[i].value_type);
    printf("operator_sibling: %s\n", arg_array[i].operator_sibling);
    printf("operator_child: %s\n", arg_array[i].operator_child);
    printf("weight: %d\n", arg_array[i].weight);
    printf("dependency_id_len: %d\n", arg_array[i].dependency_id_len);
    printf("\n");
  }
  return EXIT_NORMALLY;
}

int arg_fuzz_display(arg_node* arg_array, int arg_count, bitmap* arg_bitmap, ir* ir_) {
  int i, ret;
  for (i = 0; i < arg_count; i++) {     
    if (ir_[i].enable == 1) {
      switch (arg_array[i].value_type) {
      case 1:
        printf("%d %d %d %s %ld\n", i,arg_bitmap[i], ir_[i].enable, arg_array[i].arg, ir_[i].value_int);
        break;
      case 2:
        printf("%d %d %d %s %ld\n", i,arg_bitmap[i], ir_[i].enable, arg_array[i].arg, ir_[i].value_int);
        break;
      case 3:
        printf("%d %d %d %s %s\n", i,arg_bitmap[i], ir_[i].enable, arg_array[i].arg, ir_[i].value_char);
        break;
      case 4:
        printf("%d %d %d %s %s\n", i,arg_bitmap[i], ir_[i].enable, arg_array[i].arg, ir_[i].value_char);
        break;
      default: 
        printf("%d %d %d %s\n", i,arg_bitmap[i], ir_[i].enable, arg_array[i].arg);
      }
    }
  else
    printf("%d %d %d %s\n", i,arg_bitmap[i], ir_[i].enable, arg_array[i].arg);
  }  
  printf("\n");
}

int ct_builder(json_object *jso, int flags, 
                                json_object *parent_jso, const char *jso_key, 
                                size_t *jso_index, arg_node* arg_array) {
  int i, ret;
  int id = 0;
  int len;
  char* key;
  bool id_loaded = false;
  struct json_object* jobj;
  struct json_object* jvalue;
  struct json_object_iterator it;
  struct json_object_iterator itEnd;

  if (json_object_get_type(jso) == json_type_object) {

    if (flags != JSON_C_VISIT_SECOND) {
      // printf("json_index: %ld\n", *jso_index);
      // printf(jso_key);
      it = json_object_iter_begin(jso);
      itEnd = json_object_iter_end(jso);
      while (!json_object_iter_equal(&it, &itEnd)) {
        key = (char*)json_object_iter_peek_name(&it);
        if (!strcmp(key, "id")) {
          id = json_object_get_int(json_object_iter_peek_value(&it));
          id_loaded = true;
          // printf("id:: %d\n", id);
          arg_array[id].arg = (char*)jso_key;
        }
        json_object_iter_next(&it);
      }

      if (id_loaded) {
        it = json_object_iter_begin(jso);
        while (!json_object_iter_equal(&it, &itEnd)) {
          len = 0;
          key = (char*)json_object_iter_peek_name(&it);
          if (!strcmp(key, "value_type")) {
            // printf(jso_key);
            if (json_object_iter_peek_value(&it) != NULL)
              arg_array[id].value_type = json_object_get_int(json_object_iter_peek_value(&it));
            else
              arg_array[id].value_type = 0;
            // printf(": value type %d\n", arg_array[id-1].value_type);
          }

          if (!strcmp(key, "value")) {
            if (json_object_iter_peek_value(&it) != NULL) {
              jobj = json_object_iter_peek_value(&it);
              if (arg_array[id].value_type == 1 || arg_array[id].value_type == 2) {
                len = json_object_array_length(jobj);
                arg_array[id].value_int = malloc(sizeof(unsigned long) * len);
                for (i=0; i < len; i++){
                  jvalue = json_object_array_get_idx(jobj, i);
                  // printf("value[%d]: %d\n",i, json_object_get_int(jvalue));
                  arg_array[id].value_int[i] = json_object_get_int(jvalue);
                }    
              }       
              if (arg_array[id].value_type == 3) {
                // printf("value: %s\n", json_object_get_string(jobj));
                arg_array[id].value_char = (char*)json_object_get_string(jobj);
              }
              if (arg_array[id].value_type == 4) {
                len = json_object_array_length(jobj);
                arg_array[id].char_array_len = len;
                arg_array[id].value_char_array = malloc(len * sizeof(char*));
                for (i=0; i < len; i++){
                  jvalue = json_object_array_get_idx(jobj, i);
                  arg_array[id].value_char_array[i] = (char*)json_object_get_string(jvalue);
                }           
              }  
            }
            else
              arg_array[id].char_array_len = 0;
          }

          if (!strcmp(key, "operator_value")) {
            if (json_object_iter_peek_value(&it) != NULL)
              arg_array[id].operator_value = (char*)json_object_get_string(json_object_iter_peek_value(&it));
            else
              arg_array[id].operator_value = "NULL";
          }

          if (!strcmp(key, "operator_sibling")) {
            if (json_object_iter_peek_value(&it) != NULL)
              arg_array[id].operator_sibling = (char*)json_object_get_string(json_object_iter_peek_value(&it));
            else
              arg_array[id].operator_sibling = "NULL";
          }

          if (!strcmp(key, "operator_child")) {
            if (json_object_iter_peek_value(&it) != NULL)
              arg_array[id].operator_child = (char*)json_object_get_string(json_object_iter_peek_value(&it));
            else
              arg_array[id].operator_child = "NULL";
          }

          if (!strcmp(key, "mutex")) {
            if (json_object_iter_peek_value(&it) != NULL){
              jobj = json_object_iter_peek_value(&it);
              len = json_object_array_length(jobj);
              arg_array[id].mutex_len = len;
              arg_array[id].mutex = malloc(sizeof(int) * len);
              for (i=0; i < len; i++) {
                jvalue = json_object_array_get_idx(jobj, i);
                // printf("value[%d]: %d\n",i, json_object_get_int(jvalue));
                arg_array[id].mutex[i] = json_object_get_int(jvalue);
              }           
            }
            else
              arg_array[id].mutex_len = 0;
          }

          if (!strcmp(key, "must_have")) {
            if (json_object_iter_peek_value(&it) != NULL)
              arg_array[id].must_have = json_object_get_boolean(json_object_iter_peek_value(&it));
            else
              arg_array[id].must_have = false;
          }

          if (!strcmp(key, "weight")) {
            if (json_object_iter_peek_value(&it) != NULL)
              arg_array[id].weight = json_object_get_int(json_object_iter_peek_value(&it));
            else
              arg_array[id].weight = 1;
            // printf("weight:: %d\n", arg_array[id-1].weight);
          }

          if (!strcmp(key, "dependency_id")) {
            if (json_object_iter_peek_value(&it) != NULL) {
              jobj = json_object_iter_peek_value(&it);
              len = json_object_array_length(jobj);
              arg_array[id].dependency_id_len = len;
              arg_array[id].dependency_id = malloc(sizeof(int) * len);
              for (i=0; i < len; i++) {
                jvalue = json_object_array_get_idx(jobj, i);
                // printf("dependency_id[%d]: %d\n",i, json_object_get_int(jvalue));
                arg_array[id].dependency_id[i] = json_object_get_int(jvalue);
              }           
            }
            else
              arg_array[id].dependency_id_len = 0;
          }

          if (!strcmp(key, "must_child")) {
            if (json_object_iter_peek_value(&it) != NULL)
              arg_array[id].must_child = json_object_get_boolean(json_object_iter_peek_value(&it));
            else
              arg_array[id].must_have = false;
          }

          if (!strcmp(key, "child_id")) {
            if (json_object_iter_peek_value(&it) != NULL) {
              jobj = json_object_iter_peek_value(&it);
              len = json_object_array_length(jobj);
              arg_array[id].child_id_len = len;
              arg_array[id].child_id = malloc(sizeof(int) * len);
              for (i=0; i < len; i++) {
                jvalue = json_object_array_get_idx(jobj, i);
                // printf("dependency_id[%d]: %d\n",i, json_object_get_int(jvalue));
                arg_array[id].child_id[i] = json_object_get_int(jvalue);
              }           
            }
            else
              arg_array[id].child_id_len = 0;
          }
          json_object_iter_next(&it);
        }
      }
    }
  }
  return JSON_C_VISIT_RETURN_CONTINUE;
}

int json_tree_parse(struct json_object* json_arg_tree, arg_node* arg_array, 
                                                      int* arg_count) {
  int ret;
  struct json_object* json_node;
  ret = json_c_visit(json_arg_tree, 0, ct_builder, arg_array);
  return ret;
}

int bitmap_len(arg_node* arg_array, int* arg_count) {
  int i;
  int arg_bitmap_len = 0;

  for (int i = 0; i < *arg_count; i++) {
    arg_bitmap_len += arg_array[i].weight;
  }
  return arg_bitmap_len;
}

int bitmap_fuzz(bitmap* arg_bitmap, int* arg_count) {
  int i;

  for (i = 0; i < *arg_count; i++) {
    arg_bitmap[i] = (unsigned char) (rand() % 255 + 1);
  }  
  return EXIT_NORMALLY;
}

unsigned long rand_num(unsigned long min, unsigned long max) {
  unsigned long x;
  unsigned int i;
  uint8_t *px = (uint8_t *)&x;

  for (i = 0; i < sizeof(x); i++)
    px[i] = random();

  return min + (unsigned long)((double)(max - min) *
        (x / ((double) UINT64_MAX + 1.0)));
}

int enable_dependency(arg_node* arg_array, ir* ir_, int id) {
  int i, ret;
  int parent_id;
  int dependency_id_len = arg_array[id].dependency_id_len;
  int child_id_len = arg_array[id].child_id_len;

  if (dependency_id_len != 0 && child_id_len == 0) {
    for (i = 0; i < arg_array[id].dependency_id_len; i++) {
      parent_id = arg_array[id].dependency_id[i];
      if (ir_[parent_id].enable == 0) {
        ir_[parent_id].enable = 1;
        ret = enable_dependency(arg_array, ir_, parent_id);
      }
    }
  }
  return EXIT_NORMALLY;
}

int enable_dependant(arg_node* arg_array, ir* ir_, int id) {
  int i, ret;
  int child_id;
  int child_id_len = arg_array[id].child_id_len;
  bool no_child = true;

  if (arg_array[id].must_child) {
    for (i = 0; i < child_id_len; i++) {
      child_id = arg_array[id].child_id[i];
      if (ir_[child_id].enable == 1)
        no_child = false;
        break;
    }
    if (no_child) {
      child_id = arg_array[id].child_id[rand_num(0, child_id_len)];
      ir_[child_id].enable = 1;
      ret = enable_dependency(arg_array, ir_, child_id);
    }
  }
  return EXIT_NORMALLY;
}


int arg_fuzz(arg_node* arg_array, int* arg_count, bitmap* arg_bitmap, 
                                    int fuzz_level, ir* ir_, char* cmd) {
  int i, j, k, tmp, ret;
  int* mutex;
  // char cmd[MAX_CMD_LEN];
  char val[MAX_VAL_LEN]; 
  unsigned long  a;

  ret = bitmap_fuzz(arg_bitmap, arg_count);

  for (i = 0; i < *arg_count; i++) {
  /* currently don't support weight feature, since the bitmap is not a real bitmap, 
  we simply use even/odd to represent enable/disable. For the future version to 
  be integrated with AFL, we will support this feature with a real bitmap with 
  more sophisticated desicion rule. */
    if (arg_bitmap[i] % 2 == 0) {
      ir_[i].enable = 1;
    }
    switch (arg_array[i].value_type) {
      case 1:
        /* Need some protection if value is greater than limitation on unsigned long */
        tmp = (arg_array[i].value_int[1] - arg_array[i].value_int[0]) / arg_array[i].value_int[2];
        ir_[i].value_int = arg_array[i].value_int[0] + rand_num(0, tmp+1) * arg_array[i].value_int[2];
        // printf("%s %ld\n", arg_array[i].arg, ir_[i].value_int);
        break;
      case 2:
        /* Need some protection if value is greater than limitation on unsigned long */
        // printf("min: %ld, max: %ld\n", arg_array[i].value_int[1], arg_array[i].value_int[2]+1);
        tmp = rand_num(arg_array[i].value_int[1], arg_array[i].value_int[2]+1);
        // printf("tmp = %d\n", tmp);
        ir_[i].value_int = pow(arg_array[i].value_int[0], tmp) * arg_array[i].value_int[3];
        // printf("%s %ld\n", arg_array[i].arg, ir_[i].value_int);
        break;
      case 3:
        ir_[i].value_char = arg_array[i].value_char;
        // printf("%s %s\n", arg_array[i].arg, ir_[i].value_char);
        break;
      case 4:
        ir_[i].value_char = arg_array[i].value_char_array[rand_num(0, arg_array[i].char_array_len)];
        // printf("rand_num output: %ld %s %s\n", a, arg_array[i].arg, ir_[i].value_char);
        break;
    }
  }

  if (fuzz_level == 0) {
    /* first time iteration. enable all must-haves and randomly prune one of the node 
    in each mutex pair. Based on our observation, all mutex nodes are leaf nodes, so
    no need for recursive disable */
    for (i = 0; i < *arg_count; i++) { 
      switch (ir_[i].enable) {
        case 0: 
          if (arg_array[i].must_have == true) 
            ir_[i].enable = 1; 
            break;
        case 1:
          if (arg_array[i].mutex != 0) {
            tmp = 1;
            for (j = 0; j < arg_array[i].mutex_len; j++) {
              if (ir_[arg_array[i].mutex[j]].enable == 1) {
                tmp += 1;
              }
            }
            mutex = malloc(tmp * sizeof(int));
            mutex[0] = i;
            for (j = 0; j < arg_array[i].mutex_len; j++) {
              if (ir_[arg_array[i].mutex[j]].enable = 1) {
                mutex[j+1] = arg_array[i].mutex[j];
              }
            }
            k = rand_num(0, tmp);
            for (j = 0; j < tmp; j++) {
              ir_[mutex[j]].enable = (j == k) ? 1:2;
            }
            free(mutex);
            break;
          } 
      }
    }
    /* second time iteration. enable all dependency nodes for leaf nodes and 
    enable a child node for non-leaf nodes with no child nodes but must have a child*/    
    for (i = 0; i < *arg_count; i++) {
      ret = enable_dependency(arg_array, ir_, i);
      ret = enable_dependant(arg_array, ir_, i);
    }
  }

  //// next next step is to develop global rules//////////

  /* display fuzzing result for each argument */
  // ret = arg_fuzz_display(arg_array, *arg_count, arg_bitmap, ir_);

  strcpy(cmd, "mke2fs ");
  for (i = 0; i < *arg_count; i++) {
    if (ir_[i].enable == 1) {
      strcat(cmd, arg_array[i].arg);
      /* temporary defualt setting, may add a operator_value to feature in the future */
      if (arg_array[i].operator_value !="NULL") 
        strcat(cmd, arg_array[i].operator_value); 
      if (arg_array[i].value_type == 1 || arg_array[i].value_type == 2) {
        sprintf(val, "%lu", ir_[i].value_int);
        strcat(cmd, val);
      }
      else if (arg_array[i].value_type == 3 || arg_array[i].value_type == 4) {
        strcat(cmd, ir_[i].value_char);
      }
      if (arg_array[i].child_id_len != 0 && arg_array[i].operator_child != "NULL") {
        strcat(cmd, arg_array[i].operator_child);  
      }
      if(arg_array[i].operator_sibling != "NULL")
        strcat(cmd, arg_array[i].operator_sibling);      
    }
        // printf("%s\n", cmd);
  }

  strcat(cmd, "100M"); 
  for (i = 0; i < *arg_count; i++) 
      ir_[i].enable = 0;

  return EXIT_NORMALLY;
}

int main(int argc, char* argv[]) {
  int i, ret;
  int node_count = 0;
  int bmap_len;
  int fuzz_level;
  FILE* fd;
  char* file_name = argv[1];
  char* json_file = NULL;
  char* utility = "mke2fs";
  char cmd[MAX_CMD_LEN];
  struct json_object* json_arg_tree;
  arg_node* arg_array;
  ir* ir_;
  bitmap* arg_bitmap;
  struct timeval tv;
  struct timezone tz;

  gettimeofday(&tv, &tz);
  srandom(tv.tv_sec ^ tv.tv_usec ^ getpid());

  if (!argv[1]) {
    printf("JSON file missing.\n");
    return 1;  
  }
  fd = fopen(file_name, "r");
  if (fd != NULL) {
    if (fseek(fd, 0L, SEEK_END) == 0) {
      long bufsize = ftell(fd);
      if (bufsize == -1) 
        return 1;
      json_file = malloc(sizeof(char) * (bufsize + 1));
      if (fseek(fd, 0L, SEEK_SET) != 0) 
        return 1;
      size_t newLen = fread(json_file, sizeof(char), bufsize, fd);
      if (ferror( fd ) != 0 )
        fputs("Error reading file", stderr);
      else 
        json_file[newLen++] = '\0'; 
    }
    fclose(fd);
  }
  json_arg_tree = json_tokener_parse(json_file);  
  ret = json_c_visit(json_arg_tree, 0, jso_count, &node_count);
  node_count = node_count -1; 
  arg_array = malloc(node_count * sizeof(arg_node));
  ret = json_tree_parse(json_arg_tree, arg_array, &node_count);
  ir_ = malloc(node_count * sizeof(ir));
  /* display non-array values in constraint tree */
  // ret = ct_display(arg_array, &node_count);    
  bmap_len = bitmap_len(arg_array, &node_count);
  arg_bitmap = malloc(bmap_len * sizeof(unsigned char));
  fuzz_level = SEMANTICALLY_CORRECT;
  for (i = 0; i< 1; i++) {
    ret = arg_fuzz(arg_array, &node_count, arg_bitmap, fuzz_level, ir_, cmd);
    printf("%s\n", cmd);
  }
  // unsigned long tmp;
  // for (i = 0; i<10 ;i++) {
  //   tmp = rand_num(0, 1000001);
  //   printf("%ld\n", tmp);
  // }
  free(arg_array);
  free(ir_);
  free(json_file);
  free(arg_bitmap);
  return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <json.h>
#include <json_visit.h>
#include <stdbool.h>

#define EXIT_NORMALLY 0


/* input for afl */
typedef unsigned char* bitmap;
typedef char** features;

typedef struct arg_node {
  char* arg;
  int value_type; 
  long long int* value_int;
  char* value_char;
  char** value_char_array;
  char* operator_sibling;
  char* operator_child;
  int* mutex;
  bool must_have;
  int weight;
  int* dependency_id;
}arg_node;

typedef struct ir { 
  bitmap arg_bitmap;
  int bmap_index[2];
  void* value;
}ir;

// void json_tree_parser(struct json_object* json_arg_tree, int* count);
int jso_count(json_object *jso, int flags, 
                                json_object *parent_jso, const char *jso_key, 
                                size_t *jso_index, int *count);
int ct_builder(json_object *jso, int flags, 
                                json_object *parent_jso, const char *jso_key, 
                                size_t *jso_index, arg_node* arg_array);
int ct_free(arg_node* arg_array);
int ir_bitmap_initialize(bitmap arg_bitmap, arg_node* arg_array, int arg_count);
int ir_bitmap_free(bitmap arg_bitmap);
int json_tree_parser(struct json_object* json_arg_tree);



int jso_count(json_object *jso, int flags, 
                                json_object *parent_jso, const char *jso_key, 
                                size_t *jso_index, int *count) {
  if(json_object_get_type(jso) == json_type_object)
      if(flags != JSON_C_VISIT_SECOND) 
        *count += 1;
  return JSON_C_VISIT_RETURN_CONTINUE;
}


int ir_bitmap_initialize(bitmap arg_bitmap, arg_node* arg_array, int arg_count) {
  int i;
  int arg_bitmap_len = 0;
  // arg_count = sizeof(arg_array)/sizeof(arg_array[0]);
  // printf("%d arguments in total\n", arg_count);
//   printf("here\n");
  // printf("%d\n", arg_count);
  for(int i = 0; i<47; i++) {
    // printf("id [%d] weight: %d\n", i, arg_array[i].weight);
    arg_bitmap_len += arg_array[i].weight;
  }
  // printf("%d\n", arg_bitmap_len);
  arg_bitmap = malloc(arg_bitmap_len * sizeof(unsigned char));
  printf("%bitmap length in byte: %d\n", sizeof(arg_bitmap)/sizeof(unsigned char));
  for (i = 0; i < arg_bitmap_len - 1; i++) {
      arg_bitmap[i] = (unsigned char) (rand() % 255 + 1);
  }  
  printf("%d\n", arg_bitmap);
  printf("%bitmap length in byte: %d\n", sizeof(arg_bitmap)/sizeof(unsigned char));
//     arraylen = 0;
//     printf("id: %d\n", i+1);

// /****************checkpoint here***************/
// /****************can't print arg_array fields**/
//     printf("arg: %s\n", arg_array[i].arg);
//     printf("value_type: %d\n", arg_array[i].value_type);
//     // printf("value: %s\n", arg_array[i].value);
//     // if(arg_array[i].value_type != NULL) {
//       // printf("here!\n");
//     if(arg_array[i].value_type != 0) {
//       if(arg_array[i].value_int != NULL){
//           arraylen = array_list_length(arg_array[i].value_int);
//         }
//           json_object * jvalue;
//           for (j=0; j< arraylen; j++){
//             jvalue = json_object_array_get_idx(arg_array[i].value_int, j);
//             printf("value[%d]: %d\n",j, json_object_get_int(jvalue));       
//           }
//         // case 1:
//         //     for(j = 0; j < 3; j++)
//         //       printf("value: %d\n", array_list_get_idx(arg_array[i].value, j));
//         //      break;
//         // Default:
//         //      printf("Value is None");
//         //      break;
//       // }
//       }
//     printf("Array Length: %d\n",arraylen);

//     printf("operator_sibling: %s\n", arg_array[i].operator_sibling);
//     printf("operator_child: %s\n", arg_array[i].operator_child);
//     }
    // printf("mutex: %d\n", arg_array[i].mutex[0]);

  // if(weight == false)
  //   arg_bitmap_len = (arg_count);
  // arg_bitmap = malloc(sizeof(bitmap) * arg_bitmap_len);
  return EXIT_NORMALLY;
}

int ct_builder(json_object *jso, int flags, 
                                json_object *parent_jso, const char *jso_key, 
                                size_t *jso_index, arg_node* arg_array) {
  int i, ret;
  int id = 0;
  int len;
  char* key;
  struct json_object* jobj;
  struct json_object* jvalue;
  struct json_object_iterator it;
  struct json_object_iterator itEnd;
  
  if(json_object_get_type(jso) == json_type_object) {

    if(flags != JSON_C_VISIT_SECOND) {
      it = json_object_iter_begin(jso);
      itEnd = json_object_iter_end(jso);

      while (!json_object_iter_equal(&it, &itEnd)) {
        key = json_object_iter_peek_name(&it);
        if(!strcmp(key, "id")) {
          id = json_object_get_int(json_object_iter_peek_value(&it));
          arg_array[id].arg = jso_key;
        }
        json_object_iter_next(&it);
      }

      if(id != 0) {
        it = json_object_iter_begin(jso);

        while (!json_object_iter_equal(&it, &itEnd)) {
          len = 0;
          key = json_object_iter_peek_name(&it);
          if(!strcmp(key, "value_type")) {
            // printf(jso_key);
            if(json_object_iter_peek_value(&it) != NULL)
              arg_array[id-1].value_type = json_object_get_int(json_object_iter_peek_value(&it));
            else
              arg_array[id-1].value_type = 0;
            // printf(": value type %d\n", arg_array[id-1].value_type);
          }

          if(!strcmp(key, "value")) {
            if(json_object_iter_peek_value(&it) != NULL) {
              jobj = json_object_iter_peek_value(&it);
              if(arg_array[id-1].value_type == 1 || arg_array[id-1].value_type == 2) {
                len = json_object_array_length(jobj);
                arg_array[id-1].value_int = malloc(sizeof(long long int) * len);
                for (i=0; i < len; i++){
                  jvalue = json_object_array_get_idx(jobj, i);
                  // printf("value[%d]: %d\n",i, json_object_get_int(jvalue));
                  arg_array[id-1].value_int[i] = json_object_get_int(jvalue);
                }    
              }       
              if(arg_array[id-1].value_type == 3) {
                // printf("value: %s\n", json_object_get_string(jobj));
                arg_array[id-1].value_char = json_object_get_string(jobj);
              }
              if(arg_array[id-1].value_type == 4) {
                len = json_object_array_length(jobj);
                arg_array[id-1].value_char_array = malloc(len * sizeof(char*));
                for (i=0; i < len; i++){
                  jvalue = json_object_array_get_idx(jobj, i);
                  arg_array[id-1].value_char_array[i] = json_object_get_string(jvalue);
                }           
              }  
            }
          }

          if(!strcmp(key, "operator_sibling")) {
            if(json_object_iter_peek_value(&it) != NULL)
              arg_array[id-1].operator_sibling = json_object_get_string(json_object_iter_peek_value(&it));
            else
              arg_array[id-1].operator_sibling = " ";
          }

          if(!strcmp(key, "operator_child")) {
            if(json_object_iter_peek_value(&it) != NULL)
              arg_array[id-1].operator_child = json_object_get_string(json_object_iter_peek_value(&it));
            else
              arg_array[id-1].operator_child = " ";
          }

          if(!strcmp(key, "mutex")) {
            if(json_object_iter_peek_value(&it) != NULL){
              jobj = json_object_iter_peek_value(&it);
              len = json_object_array_length(jobj);
              arg_array[id-1].mutex = malloc(sizeof(int) * len);
              for (i=0; i < len; i++) {
                jvalue = json_object_array_get_idx(jobj, i);
                // printf("value[%d]: %d\n",i, json_object_get_int(jvalue));
                arg_array[id-1].mutex[i] = json_object_get_int(jvalue);
              }           
            }
          }

          if(!strcmp(key, "must_have")) {
            if(json_object_iter_peek_value(&it) != NULL)
              arg_array[id-1].mutex = json_object_get_boolean(json_object_iter_peek_value(&it));
            else
              arg_array[id-1].mutex = false;
          }

          if(!strcmp(key, "weight")) {
            if(json_object_iter_peek_value(&it) != NULL)
              arg_array[id-1].weight = json_object_get_int(json_object_iter_peek_value(&it));
            else
              arg_array[id-1].weight = 1;
          }

          if(!strcmp(key, "dependency_id")) {
            if(json_object_iter_peek_value(&it) != NULL) {
              jobj = json_object_iter_peek_value(&it);
              len = json_object_array_length(jobj);
              arg_array[id-1].dependency_id = malloc(sizeof(int) * len);
              for (i=0; i < len; i++) {
                jvalue = json_object_array_get_idx(jobj, i);
                // printf("dependency_id[%d]: %d\n",i, json_object_get_int(jvalue));
                arg_array[id-1].dependency_id[i] = json_object_get_int(jvalue);
              }           
              // printf("here!\n");   
            }
          }
          json_object_iter_next(&it);
        }
        // printf("\n");
      }
    }
  }
  return JSON_C_VISIT_RETURN_CONTINUE;
}

int json_tree_parse(struct json_object* json_arg_tree) {
  int ret;
  int arg_count = 0;
  struct json_object* json_node;
  arg_node* arg_array;
  ir* ir_;

  ret = json_c_visit(json_arg_tree, 0, jso_count, &arg_count);
  arg_count = arg_count -1; // remove the root node, its not an argument

  arg_array = malloc(arg_count * sizeof(arg_node));

  ret = json_c_visit(json_arg_tree, 0, ct_builder, arg_array);
  ret = ir_bitmap_initialize(ir_->arg_bitmap, arg_array, arg_count);
  return ret;
}

int main(int argc, char* argv[]) {

  int i, ret;
  int node_count = 0;
  FILE* fd;
  char* file_name = argv[1];
  char* json_file = NULL;
  char* utility = "mke2fs";
  struct json_object* json_arg_tree;
  struct json_object* root_node;

  if (!argv[1]) {
    printf("JSON file missing.\n");
    return 1;  }

  fd = fopen(file_name, "r");

  if (fd != NULL) {
      /* Go to the end of the file. */
      if (fseek(fd, 0L, SEEK_END) == 0) {
          /* Get the size of the file. */
          long bufsize = ftell(fd);
          if (bufsize == -1) 
            return 1;
          /* Allocate our buffer to that size. */
          json_file = malloc(sizeof(char) * (bufsize + 1));

          /* Go back to the start of the file. */
          if (fseek(fd, 0L, SEEK_SET) != 0) 
            return 1;

          /* Read the entire file into memory. */
          size_t newLen = fread(json_file, sizeof(char), bufsize, fd);
          if ( ferror( fd ) != 0 ) {
              fputs("Error reading file", stderr);
          } else {
              json_file[newLen++] = '\0'; /* Just to be safe. */
          }
      }
      fclose(fd);
  }

  json_arg_tree = json_tokener_parse(json_file);   

  ret = json_tree_parse(json_arg_tree);

  return 0;
}
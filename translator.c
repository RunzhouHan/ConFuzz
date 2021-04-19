#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <json.h>
#include <json_visit.h>
#include <stdbool.h>



/* input for afl */
typedef unsigned char bitmap;

void json_tree_parser(struct json_object* json_arg_tree, int* count);
// json_c_visit_userfunc* jso_count;

typedef struct arg_node {
  int id;
  char* arg;
  char* operator_sibling;
  char* operator_child;
  int* mutex;
  bool must_have;
  int* dependency_id;
  int weight;
  bool enabled;
  int* child_arg;
  char* value_type; 
  void* value;
  int ir_index;
}arg_node;

typedef struct root_node { 
  char* utility;
  int* arg_list;
}root_node;

// int jso_count(json_object *jso, int flags, 
//                                 json_object *parent_jso, const char *jso_key, 
//                                 size_t *jso_index, int *count) {
//   printf("jso_count is invoked! \n");
//   *count += 1;
//   return 0;
// }

// void json_tree_parser(struct json_object* json_arg_tree) {
//   int ret;
//   int arg_count = 0;
//   bitmap* arg_bitmap;
//   struct json_object* json_node;

//   // helper = jso_count;
//   // ret = json_c_visit(json_arg_tree, 0, jso_count, &arg_count);
//   // json_object_object_foreach(json_arg_tree, arg, constraint) {      
//   //   arg_count += 1;
//   //   json_c_visit()
//   // }                
//   printf("%d args in total \n", arg_count);                                             

// }

void json_tree_parser(struct json_object* obj, int* count) {

  struct json_object* child;
  struct json_object_iterator it;
  struct json_object_iterator itEnd;

  it = json_object_iter_begin(obj);
  itEnd = json_object_iter_end(obj);

  while (!json_object_iter_equal(&it, &itEnd)) {
    // struct json_object* child;
    printf("%s: %s\n", json_object_iter_peek_name(&it), json_object_iter_peek_value(&it));
    *count += 1;
    printf("%ld, %ld\n", sizeof(json_object_iter_peek_value(&it)), sizeof(struct json_object*));
    // if(sizeof(json_object_iter_next(&it)) == sizeof(struct json_object*))
    printf("#%d is a json object\n", *count);
    if(json_object_iter_peek_value(&it)) {
      child = json_object_iter_peek_value(&it);
      json_tree_parser(child, count);
    }
    json_object_iter_next(&it);
 }


}

int main(int argc, char* argv[]) {

  int i, rc;
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

  int a = 0;
  // json_object_object_foreach(json_arg_tree, arg, constraint) {
  //   printf("arg = %s constraint = %s\n", arg, json_object_get_string(constraint));   
  // }   

  json_tree_parser(json_arg_tree, &node_count);
  printf("%d arg nodes in total\n", node_count);
  // free(json_file);
  // free(file_name);
  // free(mke2fs_json);
  // free(root_node);
  return 0;
}
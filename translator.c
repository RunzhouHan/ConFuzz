#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <json.h>

// const int MAXBUFLEN = 10000000;  // Causes segmentation fault


int json_c_visit (json_object* jso, int future_flags, json_c_visit_userfunc* userfunc, void* userarg);

int json_c_visit (json_object* jso, int future_flags, 
  json_c_visit_userfunc* userfunc, void* userarg) {

}


int main (int argc, char* argv[]) {

  int i, rc;
  FILE* fd;
  char* file_name;
  char json_file[1024];
  struct json_object* mke2fs_json;
  struct json_object* root_node;

  if (!argv[1]) {
    printf("JSON file missing.\n");
    return 1;  }

  fd = fopen(argv[1], "r");
  if (fd != NULL) {
    fread(json_file, 1024, 1, fd);               
    fclose(fd);
  }
  else {
    printf("Can't open %s\n", argv[1]);
    return 1;
  }

  mke2fs_json = json_tokener_parse(json_file);   


  json_object_object_foreach(mke2fs_json, arg, constraint) {      
    // printf("arg = %s", json_object_get_string(mke2fs_json));                           
    printf("arg = %s constraint = %s\n",arg, json_object_get_string(constraint));   
    // printf("I'm here\n");    
  }                                                                           

  return 0;
}
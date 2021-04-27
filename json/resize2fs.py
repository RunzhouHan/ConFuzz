import json

# value type      #        format  	  	meaning
# arithmatic_int    1      [a,b,c]    	arithmatic sequence between [int a,int b] with factor int c
# geometric_int     2	   [a,b,c,d]  	
# string            3	   "something"	"something"
# string_array      4      ["a","b"]    select one out of "a" and "b"

RAID_stride="RAID-stride"
undo_file="undo_file"

resize2fs_command = {
	"-b": {
		"id": 0,
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": [7],
		"must_have": False, 
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-d": {
		"id": 1,
		"value_type": 2,
		"value": [2,1,5,1],
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-f": {
		"id": 2,
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False, 
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-F": {
		"id": 3,
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False, 
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-M": {
		"id": 4,
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False, 
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-p": {
		"id": 5,
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False, 
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-P": {
		"id": 6,
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False, 
		"dependency_id": [4],
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-s": {
		"id": 7,
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": [0],
		"must_have": False, 
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-S": {
		"id": 8,
		"value_type": 3,
		"value": RAID_stride,
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False, 
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-z": {
		"id": 9,
		"value_type": 3,
		"value": undo_file,
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False, 
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		}
}

with open('resize2fs.json', 'w') as f:
	json.dump(resize2fs_command, f, ensure_ascii=False, indent=4)
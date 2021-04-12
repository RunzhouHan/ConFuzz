import json

# template for an argument:
# "-b": {
# 	"value": , #required, can be 
# 	"value_combination": 1
# 	"child": None,
# 	"operator_sibling": " ",
# 	"operator_child": None,
# 	"operator_value": " ", 
# 	"mutex": None,
# 	"must_have": True
# 	# "special_ops": None
# }

command = {
	"mke2fs": [
		{"id": 1,
		"arg": "-b",
		"value": [1024, 2048, 4096],
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,
		"child": None},

		{"id": 2,
		"arg": "-c",
		"value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,
		"child": [
			{"id": 3,
			"arg": "-c",
			"value": None,
			"operator_sibling": None,
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": 2,
			"child": None}
		]},
	
		{"id": 4,
		"arg": "-E",
		"value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True,
		"dependencies_id": None,
		"child": [
			{"id": 0,
			"arg": "stride=", # RAID arg, need to test with '='' & '= ' 
			"value": -1,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,  # not sure
			"must_have": False,
			"dependencies": None,  # not sure
			"parent_id": 3 
			"child": None,
			},
		"stride-width=": {  # RAID args 
			"id": 1,
			"value": 0,
			"value_property": None, # This is typically stride-size * N
			"child": None,
			"operator_sibling": ",",
			"operator_child": None,
			"operator_value": " ", 
			"mutex": None,  # not sure
			"must_have": False,
			"dependencies": 4,  # not sure
			"parent_id": 3 
			},
		"resize"
		]},
	]
}


# arg_1_1 = {}

json_object = json.dumps(command, indent = 4)
print(json_object)
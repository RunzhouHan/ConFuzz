import json

arg_0 = {
	'id': 0,
	'name': 'mke2fs',
	'prefix' : None,
	'mutex' : None,
	'parent' : None,
	'must_have': True
}

arg_1 = {
	'id' : 1,
	'name': '-b',
	'prefix':' ',
	'mutex' : None,
	'parent' : None,
	'must_have': True
}

arg_1 = {
	'id' : 1,
	'name': '-b',
	'prefix':' ',
	'mutex' : None,
	'parent' : None,
	'must_have': True
}

# arg_1_1 = {}

json_object = json.loads(arg_0, indent = 4)
json_object = json.loads(arg_1, indent = 4)

print(json_object)
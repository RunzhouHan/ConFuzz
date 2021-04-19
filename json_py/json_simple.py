import json

command = {"a": "I'm a", "b": 2, "c": True}

with open("simple.json", 'w') as f:
	json.dump(command, f, ensure_ascii=False, indent = 4)

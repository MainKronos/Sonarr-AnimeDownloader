import json

table = None

with open("table.json", 'r') as f:
	table = json.loads(f.read())

for row in table:
	row["absolute"] = False

with open("table.json", 'w') as f:
	f.write(json.dumps(table, indent=4))

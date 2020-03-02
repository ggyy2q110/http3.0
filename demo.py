import json

d = {'a': 1, 'b': 2}
data = json.dumps(d)
print(type(data))
c = json.loads(data)
print(type(c))

d = [1, 2, 3, 4]
data01 = json.dumps(d)
print(type(data01))
e = json.loads(data01)
print(type(e))
print(e)

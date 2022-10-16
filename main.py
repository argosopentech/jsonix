import pathlib
import json

db = pathlib.Path.home() / "JSONIX-Example.jsonl"


def persist(o):
    json_str = json.dumps(o)
    with open(db, "a") as dbf:
        dbf.write(json_str)
        dbf.write("\n")


def query(q):
    objects = list()
    with open(db, "r") as dbf:
        for line in dbf.readlines():
            o = json.loads(line)
            if q(o):
                objects.append(o)
    return objects


persist({"name": "P.J. Finlay", "age": 24})

print(query(lambda x: x["age"] == 24))
# [{'name': 'P.J. Finlay', 'age': 24}]

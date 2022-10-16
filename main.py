import pathlib
import json


class Jsonix:
    def __init__(self, db):
        self.db = db

    def persist(self, o):
        json_str = json.dumps(o)
        with open(self.db, "a") as dbf:
            dbf.write(json_str)
            dbf.write("\n")

    def query(self, q):
        objects = list()
        with open(self.db, "r") as dbf:
            for line in dbf.readlines():
                o = json.loads(line)
                if q(o):
                    objects.append(o)
        return objects


db = Jsonix(pathlib.Path.home() / "JSONIX-Example.jsonl")


db.persist({"name": "P.J. Finlay", "age": 24})

print(db.query(lambda x: x["age"] == 24))
# [{'name': 'P.J. Finlay', 'age': 24}]

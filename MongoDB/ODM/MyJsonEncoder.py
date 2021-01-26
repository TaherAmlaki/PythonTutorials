import json
from bson import ObjectId


# TypeError: ObjectId('') is not JSON serializable
# https://stackoverflow.com/a/16586277/8564495
class MongoObjectJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

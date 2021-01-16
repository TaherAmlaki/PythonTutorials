import requests
import json
from marshmallow import (Schema, fields, post_load,
                         ValidationError, validate, EXCLUDE)


class Person:
    def __init__(self, name, films):
        self.name = name
        self.films = films

    def __repr__(self):
        return f"{self.name} was in movies {', '.join(self.films)}"


class PersonSchema(Schema):
    name = fields.String(required=True)
    films = fields.List(fields.String(), required=True,
                        validate=validate.Length(min=1))

    @post_load
    def create_person(self, data, **kwargs):
        return Person(**data)

    class Meta:
        unknown = EXCLUDE


url = "https://swapi.dev/api/people/1"
headers = {"Content-Type": "application/json"}
res = requests.get(url, headers=headers)
response_data = res.json()
print(response_data)
person_schema = PersonSchema()

try:
    # deserialize the /people/1 response
    Luke = person_schema.load(response_data)
except ValidationError as error:
    print("ValidationError=>", error)
    print("Valid data in ValidationError=>", error.valid_data)
    raise error from None
else:
    print(f"Luke.name={Luke.name}")
    # serializing the Person object
    print("serializing=>\n", json.dumps(person_schema.dump(Luke), indent=4))

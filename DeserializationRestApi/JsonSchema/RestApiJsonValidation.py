import requests
from jsonschema import validate, ValidationError
from DictToObj import DictToObj

# getting the schema for /people endpoint from swapi
schema_url = "https://swapi.dev/api/people/schema"
schema = requests.get(schema_url).json()

# getting the actual data for a specific person
luke_url = "https://swapi.dev/api/people/1"
Luke = requests.get(luke_url).json()

try:
    validate(Luke, schema)
except ValidationError as err:
    raise err 
else:
    Luke = DictToObj(Luke)
    print(Luke.name, Luke.eye_color)

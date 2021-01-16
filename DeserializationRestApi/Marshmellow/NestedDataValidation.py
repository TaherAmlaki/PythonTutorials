from marshmallow import Schema, fields, post_load, ValidationError
import json


class Account:
    def __init__(self, **kwargs):
        self.acc_number = kwargs.get("acc_number")
        self.acc_type = kwargs.get("acc_type")

    def __repr__(self):
        return f"Account(acc_number={self.acc_number}, acc_type={self.acc_type})"


class Person:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.account = kwargs.get("account")

    def __repr__(self):
        return f"Person(name={self.name}, account={self.account})"


#######################################################################
# Creating the schema's
class AccountSchema(Schema):
    acc_type = fields.String(required=True, data_key="AccountType")
    acc_number = fields.String(required=True, data_key="AccountNumber")

    @post_load
    def create_account(self, data, **kwargs):
        return Account(**data)


class PersonSchema(Schema):
    name = fields.String(required=True)
    account = fields.Nested(AccountSchema)

    @post_load
    def create_person(self, data, **kwargs):
        return Person(**data)


person_schema = PersonSchema()

data = {
    "name": "Liam Neeson",
    "account": {
        "AccountType": "Saving",
        "AccountNumber": "1234"
    }
}

try:
    liam = person_schema.load(data)
except ValidationError as error:
    raise error from None
else:
    print("Liam Neeson =>", liam)
    print(json.dumps(person_schema.dump(liam), indent=4))

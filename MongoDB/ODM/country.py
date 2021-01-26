import mongoengine
import json
from countryData import CountryData
from MyJsonEncoder import MongoObjectJsonEncoder


class CountryReport(mongoengine.Document):
    Country = mongoengine.StringField(required=True, db_field="Country")
    CountryCode = mongoengine.StringField(required=True, db_field="CountryCode")

    data = mongoengine.EmbeddedDocumentField(CountryData)

    meta = {
        "db_alias": "core",
        "collection": "covid"
    }

    @classmethod
    def find_by_country(cls, country):
        return cls.objects().filter(Country=country).first()

    @classmethod
    def find_by_country_code(cls, country_code):
        return cls.objects().filter(CountryCode=country_code).first()

    def to_json(self):
        data = {
            "Country": self.Country,
            "CountryCode": self.CountryCode,
            "data": self.data.to_dict() if self.data is not None else None
        }
        return json.dumps(data, indent=4, ensure_ascii=True, cls=MongoObjectJsonEncoder)

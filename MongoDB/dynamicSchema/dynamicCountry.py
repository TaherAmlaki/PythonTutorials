import mongoengine
from ODM.countryData import CountryData


class CountryReport(mongoengine.DynamicDocument):
    Country = mongoengine.StringField(required=True, db_field="Country")
    CountryCode = mongoengine.StringField(required=True, db_field="CountryCode")

    data: CountryData = mongoengine.EmbeddedDocumentField(CountryData)

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

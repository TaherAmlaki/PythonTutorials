import mongoengine
from datetime import datetime


class CountryData(mongoengine.EmbeddedDocument):
    NewConfirmed = mongoengine.IntField(required=True, db_field="NewConfirmed")
    TotalConfirmed = mongoengine.IntField(required=True, db_field="TotalConfirmed")
    NewDeaths = mongoengine.IntField(required=True, db_field="NewDeaths")
    TotalDeaths = mongoengine.IntField(required=True, db_field="TotalDeaths")
    NewRecovered = mongoengine.IntField(required=True, db_field="NewRecovered")
    TotalRecovered = mongoengine.IntField(required=True, db_field="TotalRecovered")
    Date = mongoengine.DateTimeField(default=datetime.now, db_field="Date")

    meta = {
        "db_alias": "core",
        "collection": "covid"
    }

    def to_dict(self):
        return {
            "NewConfirmed": self.NewConfirmed,
            "TotalConfirmed": self.TotalConfirmed,
            "NewDeaths": self.NewDeaths,
            "TotalDeaths": self.TotalDeaths,
            "NewRecovered": self.NewRecovered,
            "TotalRecovered": self.TotalRecovered,
            "Date": self.Date  #.strftime("%Y-%m-%d")
        }

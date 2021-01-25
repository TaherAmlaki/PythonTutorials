from typing import Dict
import requests
from pymongo import MongoClient
import json
from bson import ObjectId
from dotenv import load_dotenv
import os

env = load_dotenv("./.env")
connection_str = "mongodb+srv://{}:{}@cluster0.ekhk0.mongodb.net/{}?retryWrites=true&w=majority"
cluster = MongoClient(connection_str.format(os.getenv("MONGO_DB_USERNAME"),
                                            os.getenv("MONGO_DB_PASSWORD"),
                                            os.getenv("MONGO_DB_NAME")))

db = cluster[os.getenv("MONGO_DB_NAME")]  # getting the database
covid_collection = db.covid  # getting the collection


# delete everything in the collection
# covid_collection.delete_many({})


def get_and_save_countries_data():
    try:
        headers = {"X-Access-Token": "5cf9dfd5-3449-485e-b5ae-70a60e997864"}
        summary: Dict = requests.get("https://api.covid19api.com/summary", headers=headers).json()
    except Exception as ex:
        raise ex

    global_data = summary.get("Global")
    countries_data = summary.get("Countries")
    global_data.pop("ID")
    save_to_db_global = {
        "Country": "Global",
        "details": global_data
    }
    covid_collection.insert_one(save_to_db_global)

    save_to_db_data = []
    details_keys = ["NewConfirmed", "TotalConfirmed", "NewDeaths", "TotalDeaths", "NewRecovered", "TotalRecovered",
                    "Date"]
    for country in countries_data:
        doc = {
            "Country": country["Country"],
            "CountryCode": country["CountryCode"],
            "details": {k: v for k, v in country.items() if k in details_keys}
        }
        save_to_db_data.append(doc)

    covid_collection.insert_many(save_to_db_data)


class MongoObjectJsonEncoder(json.JSONEncoder):
    """
    We need to use a extended JsonEncoder that can handle
    ObjectId coming from mongodb in each document.
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


if covid_collection.count_documents({}) == 0:
    get_and_save_countries_data()

print(f"We got {covid_collection.count_documents({})} countries!")

nl_data = covid_collection.find_one({"CountryCode": "NL"})
print("NL Covid-19 data:\n", json.dumps(nl_data, indent=4, ensure_ascii=True, cls=MongoObjectJsonEncoder))

# ==========================================================================
# Adding a new document, reading it, and then removing it
fake_country = {
    "Country": "New New Country",
    "CountryCode": "NNC"
}
covid_collection.insert_one(fake_country)

fake_country_doc = covid_collection.find_one({"CountryCode": "NNC"})
print("FakeCountry Covid-19 data:\n",
      json.dumps(fake_country_doc, indent=4, ensure_ascii=True, cls=MongoObjectJsonEncoder))

covid_collection.delete_one({"CountryCode": "NNC"})

fake_country_doc = covid_collection.find_one({"CountryCode": "NNC"})
if fake_country_doc is None:
    print("Fake Country is removed successfully!")
else:
    print("Something went wrong with deleting fake country!")

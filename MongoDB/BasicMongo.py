from typing import Dict
import requests
from pymongo import MongoClient
import json
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv("./.env")
conn_str = \
    "mongodb+srv://{username}:{password}@{clustername}.ekhk0.mongodb.net/" \
    "{dbname}?retryWrites=true&w=majority"
cluster = MongoClient(conn_str.format(username=os.getenv("MONGODB_USERNAME"),
                                      password=os.getenv("MONGODB_PASSWORD"),
                                      clustername=os.getenv("MONGODB_CLUSTER_NAME"),
                                      dbname=os.getenv("MONGODB_NAME")))

db = cluster[os.getenv("MONGODB_NAME")]  # getting the database
covid_collection = db.covid  # getting the collection

# delete everything in the collection
covid_collection.delete_many({})


def get_and_save_countries_data():
    try:
        headers = {"X-Access-Token": "5cf9dfd5-3449-485e-b5ae-70a60e997864"}
        summary: Dict = requests.get("https://api.covid19api.com/summary",
                                     headers=headers).json()
    except Exception as ex:
        # if you want to retry or give some specific message
        raise ex

    global_data = summary.get("Global")
    countries_data = summary.get("Countries")
    global_data.pop("ID")
    save_to_db_global = {
        "Country": "Global",
        "details": global_data
    }

    # how to add a single document (a dictionary in Python) to the collection
    covid_collection.insert_one(save_to_db_global)

    save_to_db_data = []
    data_keys = ["NewConfirmed", "TotalConfirmed",
                 "NewDeaths", "TotalDeaths",
                 "NewRecovered", "TotalRecovered",
                 "Date"]
    for country in countries_data:
        doc = {
            "Country": country["Country"],
            "CountryCode": country["CountryCode"],
            "data": {k: v for k, v in country.items() if k in data_keys}
        }
        save_to_db_data.append(doc)

    # how to add multiple documents (list of dictionaries) to the collection
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

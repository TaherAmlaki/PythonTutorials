import mongoengine
import requests
from typing import Dict
from dotenv import load_dotenv
import os

from country import CountryReport
from countryData import CountryData


def mongo_init():
    load_dotenv("../.env")
    conn_str = \
        "mongodb+srv://{username}:{password}@{clustername}.ekhk0.mongodb.net/" \
        "{dbname}?retryWrites=true&w=majority".format(username=os.getenv("MONGODB_USERNAME"),
                                                      password=os.getenv("MONGODB_PASSWORD"),
                                                      clustername=os.getenv("MONGODB_CLUSTER_NAME"),
                                                      dbname=os.getenv("MONGODB_NAME"))
    mongoengine.register_connection(alias="core",
                                    host=conn_str,
                                    db=os.getenv("MONGODB_NAME"))


def get_and_save_countries_data():
    try:
        headers = {"X-Access-Token": "5cf9dfd5-3449-485e-b5ae-70a60e997864"}
        summary: Dict = requests.get("https://api.covid19api.com/summary",
                                     headers=headers).json()
    except Exception as ex:
        raise ex

    countries_data = summary.get("Countries")
    save_to_db_data = []
    details_keys = ["NewConfirmed", "TotalConfirmed",
                    "NewDeaths", "TotalDeaths",
                    "NewRecovered", "TotalRecovered",
                    "Date"]
    for country in countries_data:
        data = CountryData(**{k: v for k, v in country.items() if k in details_keys})
        doc = {
            "Country": country["Country"],
            "CountryCode": country["CountryCode"],
            "data": data
        }
        save_to_db_data.append(CountryReport(**doc))

    CountryReport.objects.insert(save_to_db_data, load_bulk=False)


mongo_init()

"""
To completely remove the collection
We can add the collection by adding new documents in it.
The collection will be created automatically!
"""
# CountryReport.drop_collection()

if CountryReport.objects.count() == 0:
    get_and_save_countries_data()

country_code = "US"
doc_data = CountryReport.find_by_country_code(country_code)
if doc_data:
    print(doc_data.to_json())
else:
    print(f"Could not find data for CountryCode={country_code}")

#
# fake_country = CountryReport()
# fake_country.Country = "X123"
# fake_country.CountryCode = "X123"
# fake_country.details = CountryDetails()
#
# fake_country.save()
#
#
# fake_data = CountryReport.find_by_country_code("X123")
# print(fake_data.to_json())

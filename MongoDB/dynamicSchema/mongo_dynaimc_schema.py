import mongoengine
from dotenv import load_dotenv
import os

from dynamicSchema.dynamicCountry import CountryReport


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


mongo_init()

bt_data: CountryReport = CountryReport.find_by_country("Bhutan")
setattr(bt_data, "status", "good")
bt_data.save()

bt_data_changed: CountryReport = CountryReport.find_by_country("Bhutan")
print(bt_data_changed.to_json(indent=4))





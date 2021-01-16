import logging
from Logging import Person


logging.basicConfig(filename="./main.log",
                    filemode="w",
                    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
                    level=logging.DEBUG)


logging.debug("Starting with main.")

me = Person("Taher", 35)
logging.warning(f"me in main=>{me}")


############################# The Log ####################################
"""
2021-01-15 15:10:32,191:root:INFO:New Person instance is created => Person(name=Taher, age=35)
2021-01-15 15:10:32,191:root:WARNING:me in main=>Person(name=Taher, age=35)
"""
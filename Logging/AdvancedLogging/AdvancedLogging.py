import logging
from Backend.User import User
from Backend.Account import Account


##############################################
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("root.log", mode="w")
file_handler.setFormatter(formatter)
# if we want to filter some log messages to log files we can setLevel on file handler 
file_handler.setLevel(logging.INFO)  
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
##############################################

my_account = Account("saving", "1234")
taher = User("Taher", my_account)

logger.warning("================")
logger.debug("This is a DEBUG message.")
logger.info("This is an INFO message.")
logger.error("This is an ERROR message.")
logger.warning("================")

logger.info(taher)

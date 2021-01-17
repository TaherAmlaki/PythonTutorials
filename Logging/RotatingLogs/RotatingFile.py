import logging
from logging.handlers import RotatingFileHandler


formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")

rotating_handler = RotatingFileHandler(filename="rotating.log",
                                       mode="w",
                                       maxBytes=250,
                                       backupCount=1)
rotating_handler.setFormatter(formatter)
rotating_handler.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(rotating_handler)


for i in range(100):
    logger.info(f"{i}=>message")


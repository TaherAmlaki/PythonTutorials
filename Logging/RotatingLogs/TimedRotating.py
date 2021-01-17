import logging
from logging.handlers import TimedRotatingFileHandler
import time


formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")

timed_handler = TimedRotatingFileHandler(filename="timed.log",
                                         when="S",
                                         interval=1,
                                         backupCount=1)
timed_handler.setFormatter(formatter)
timed_handler.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(timed_handler)

start = now = time.time()
ind = 0

while (now - start) < 5:
    logger.info(f"Ind: {ind}, Time passed: {round(now-start, 2)}")
    time.sleep(0.25)
    now = time.time()
    ind += 1

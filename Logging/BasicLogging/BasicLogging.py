import logging

logging.basicConfig(filename="./basicLog.log",
                    filemode="w",
                    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
                    level=logging.INFO)

logging.debug("debug message, this will not be shown.")
logging.info("info message, this will be displayed.")
logging.warning("warning message, this message should be displayed.")

try:
    a = 2/0
except ZeroDivisionError as ex:
    logging.exception("Damn, why would you divide by zero?")

##########################################################################
"""
2021-01-15 11:24:55,479:root:INFO:info message, this will be displayed.
2021-01-15 11:24:55,479:root:WARNING:warning message, this message should be displayed.
2021-01-15 11:24:55,479:root:ERROR:Damn, why would you divide by zero?
Traceback (most recent call last):
  File "C:/.../PythonTutorials/Logging/BasicLogging.py", line 13, in <module>
    a = 2/0
ZeroDivisionError: division by zero

"""


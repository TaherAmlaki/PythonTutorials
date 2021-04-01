import logging
import sys

from WireMockTutorial.Utils.wm_exceptions import WireMockConnectionException
from WireMockTutorial.Utils.toJson import response_to_json


def set_logger():
    wm_logger = logging.getLogger("WMLogger")
    wm_logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")

    file_handler = logging.FileHandler("wm.log", mode="w")
    file_handler.setFormatter(formatter)
    wm_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    wm_logger.addHandler(stream_handler)

    return wm_logger


logger = set_logger()

WIREMOCK_URL = "http://127.0.0.1:9999"

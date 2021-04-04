import logging
import sys

from WireMockTutorial.Utils.wm_exceptions import WireMockConnectionException
from WireMockTutorial.Utils.toJson import response_to_json


DEFAULT_LOG_FORMAT = "%(asctime)s:%(name)s:%(filename)s(%(lineno)d):%(levelname)s: %(message)s"


class WireMockUrls:
    WIREMOCK_URL = "http://127.0.0.1:9999"
    MAPPINGS_URL = f"{WIREMOCK_URL}/__admin/mappings"
    RESET_URL = f"{WIREMOCK_URL}/__admin/reset"
    MAPPINGS_RESET_URL = MAPPINGS_URL + "/reset"
    SHUTDOWN_URL = f"{WIREMOCK_URL}/__admin/shutdown"


def set_logger(log_level="INFO", log_msg_format=DEFAULT_LOG_FORMAT):
    wm_logger = logging.getLogger("WMLogger")
    log_level = logging.getLevelName(log_level)
    wm_logger.setLevel(log_level)

    formatter = logging.Formatter(fmt=log_msg_format, datefmt="%y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler("./wm.log", mode="a")
    file_handler.setFormatter(formatter)
    wm_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    wm_logger.addHandler(stream_handler)

    return wm_logger


logger = set_logger()

"""
Here I create a context manager for executing WireMock jar, starting service and at
exit we will shutdown the running WireMock
"""
from subprocess import PIPE, Popen, STDOUT
from pathlib import Path

import requests

from WireMockTutorial.Utils import WireMockUrls, response_to_json, logger
from WireMockTutorial.Utils.wm_exceptions import WireMockStartException, WireMockConnectionException


class WireMockContext:
    def __init__(self, jar_location: str, root_dir: str, port: int = 9999, verbose: bool = True):
        self.jar_location = Path(jar_location).absolute()
        self.root_dir = Path(root_dir).absolute()
        self.command = f"java -jar {jar_location} --port {port} " \
                       f"--global-response-templating --root-dir {root_dir}"
        if verbose:
            self.command += " --verbose"
        self.process = None

    def __enter__(self):
        self.process = Popen(self.command.split(), stdout=PIPE, stderr=STDOUT)
        result = next(iter(self.process.stdout.readline, b"")).decode("utf-8")
        if result.startswith("Error"):
            raise WireMockStartException("Error occurred trying to start WireMock Process."
                                         f"\n\tDetail: {result}")
        logger.warning("WireMock Server is running ...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.exception(f"Error while running WireMock: {exc_type.__name__}: {exc_val}")
        self.shutdown_wire_mock()
        try:
            self.process.terminate()
        finally:
            return False

    @classmethod
    def check_wiremock_running(cls):
        try:
            res = requests.get(WireMockUrls.MAPPINGS_URL)
            if res.status_code < 400:
                logger.info("WireMock Server is running.")
            else:
                raise WireMockConnectionException
        except requests.exceptions.ConnectionError:
            raise WireMockConnectionException("ConnectionError when tried to connect to WireMock Server.")
        except WireMockConnectionException:
            raise WireMockConnectionException("WireMock Server is not running.")

    @classmethod
    def reset_mappings_and_requests_log(cls):
        res = requests.post(WireMockUrls.RESET_URL)
        return res.status_code < 400

    @classmethod
    def shutdown_wire_mock(cls):
        res = requests.post(WireMockUrls.SHUTDOWN_URL, data=None)
        if 400 <= res.status_code:
            raise WireMockConnectionException("Failed to shutdown WireMock Server.: "
                                              f"{response_to_json(res)}")
        logger.warning("WireMock Server was shutdown successfully.")

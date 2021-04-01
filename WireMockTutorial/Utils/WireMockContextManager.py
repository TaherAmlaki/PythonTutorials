"""
Here I create a context manager for executing WireMock jar, starting service and at
exit we will shutdown the running WireMock
"""
from subprocess import PIPE, Popen, STDOUT
from pathlib import Path

import requests

from WireMockTutorial.Utils import WIREMOCK_URL, response_to_json, logger
from WireMockTutorial.Utils.wm_exceptions import WireMockStartException, WireMockConnectionException


class WireMockContext:
    MAPPINGS_URL = "/__admin/mappings"
    RESET_URL = "/__admin/reset"
    SHUTDOWN_URL = "/__admin/shutdown"

    def __init__(self, jar_location: str, root_dir: str, port: int = 9999, verbose: bool = True):
        self.jar_location = Path(jar_location).absolute()
        self.root_dir = Path(root_dir).absolute()
        self.command = f"java -jar {jar_location} --port {port} --global-response-templating --root-dir {root_dir}"
        if verbose:
            self.command += "--verbose"

    def __enter__(self):
        process = Popen(self.command.split(), stdout=PIPE, stderr=STDOUT)
        # return iter(process.stdout.readline, b"")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise WireMockStartException(f"Error while running WireMock: {exc_type}: {exc_val}")
        self.reset_mappings_and_requests_log()
        self.shutdown_wire_mock()
        return False

    def check_wiremock_running(self):
        try:
            res = requests.get(f"{WIREMOCK_URL}{self.MAPPINGS_URL}")
            if res.status_code < 400:
                logger.info("WireMock Service is running.")
            else:
                raise WireMockConnectionException
        except requests.exceptions.ConnectionError:
            raise WireMockConnectionException("ConnectionError when tried to connect to WireMock Service.")
        except WireMockConnectionException:
            raise WireMockConnectionException("WireMock Service is not running.")

    def reset_mappings_and_requests_log(self):
        res = requests.post(f"{WIREMOCK_URL}{self.RESET_URL}")
        return res.status_code < 400

    def shutdown_wire_mock(self):
        res = requests.post(f"{WIREMOCK_URL}{self.SHUTDOWN_URL}", data=None)
        if 400 <= res.status_code:
            raise WireMockConnectionException(f"Failed to shutdown WireMock Service.: {response_to_json(res)}")
        logger.info("WireMock Service was shutdown successfully.")

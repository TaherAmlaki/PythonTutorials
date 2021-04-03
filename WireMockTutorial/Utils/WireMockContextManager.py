"""
Here I create a context manager for executing WireMock jar, starting service and at
exit we will shutdown the running WireMock
"""
from subprocess import PIPE, Popen, STDOUT
from pathlib import Path

from WireMockTutorial.Utils import logger
from WireMockTutorial.Utils.wm_exceptions import WireMockStartException, WireMockConnectionException
from WireMockTutorial.Utils.WireMockCommunication import WireMockManager


class WireMockContext:

    def __init__(self, jar_location: str, root_dir: str, port: int = 9999, verbose: bool = True):
        self.jar_location = Path(jar_location).absolute()
        self.root_dir = Path(root_dir).absolute()
        self.command = f"java -jar {jar_location} --port {port} " \
                       f"--global-response-templating --root-dir {root_dir}"
        if verbose:
            self.command += " --verbose"
        self._process = None

    def __enter__(self):
        self._process = Popen(self.command.split(), stdout=PIPE, stderr=STDOUT)
        result = next(iter(self._process.stdout.readline, b"")).decode("utf-8")
        if result and result.strip().startswith("Error"):
            try:
                self._process.terminate()
            finally:
                raise WireMockStartException("Error occurred trying to start WireMock Process."
                                             f"\n\tDetail: {result}")
        try:
            WireMockManager.check_wiremock_running()
        except WireMockConnectionException:
            self._process.terminate()
            raise
        else:
            return WireMockManager()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.exception(f"Error while running WireMock: {exc_type.__name__}: {exc_val}")
        try:
            WireMockManager.shutdown_wiremock()
        finally:
            try:
                self._process.terminate()
            finally:
                return False

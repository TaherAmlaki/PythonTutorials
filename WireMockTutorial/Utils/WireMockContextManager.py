"""
Here I create a context manager for executing WireMock jar, starting service and at
exit we will shutdown the running WireMock
"""
from subprocess import PIPE, Popen, STDOUT
from pathlib import Path

from WireMockTutorial.Utils import logger
from WireMockTutorial.Utils.wm_exceptions import WireMockStartException
from WireMockTutorial.Utils.WireMockCommunication import WireMockManager


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
        WireMockManager.check_wiremock_running()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.exception(f"Error while running WireMock: {exc_type.__name__}: {exc_val}")
        WireMockManager.shutdown_wiremock()
        try:
            self.process.terminate()
        finally:
            return False

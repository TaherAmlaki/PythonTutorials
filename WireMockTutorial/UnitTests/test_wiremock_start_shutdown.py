import logging
import unittest

from WireMockTutorial.Utils import WireMockConnectionException
from WireMockTutorial.Utils.WireMockContextManager import WireMockContext


class TestWireMockStartAndShutdown(unittest.TestCase):
    wiremock_jar_path = "../docs/wiremock-standalone-2.27.2.jar"
    root_path = "../wireMockRoot"

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def test_wrong_path_exception(self):
        with self.assertRaises(WireMockConnectionException):
            with WireMockContext("./wrong_path", self.root_path) as wm:
                pass

    def test_successful_start(self):
        try:
            with WireMockContext(self.wiremock_jar_path, self.root_path) as wm:
                wm.check_wiremock_running()
        except WireMockConnectionException:
            self.fail("WireMock Server not running after initialization of context.")

    def test_wiremock_shutdown(self):
        with WireMockContext(self.wiremock_jar_path, self.root_path) as wm:
            pass
        self.assertRaises(WireMockConnectionException, wm.check_wiremock_running)



import logging
import unittest

from WireMockTutorial.Utils.WireMockContextManager import WireMockContext


class TestWireMockStubbing(unittest.TestCase):
    wiremock_jar_path = "../docs/wiremock-standalone-2.27.2.jar"
    root_path = "../wireMockRoot"
    test_url = "/pythonTest"

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def test_fixed_response(self):
        with WireMockContext(self.wiremock_jar_path, self.root_path) as wm:
            wm.set_new_data_in_wm(self.test_url, body="Hello Multiverse!")
            rpy = wm.call_mocked_service(self.test_url)
            self.assertEqual(rpy.content.decode("utf-8"), '"Hello Multiverse!"')

    def test_echo_from_json_request(self):
        with WireMockContext(self.wiremock_jar_path, self.root_path) as wm:
            body = {"message": "Hello {{jsonPath request.body '$.name'}}!"}
            expected_rpy_body = {"message": "Hello Joe!"}

            wm.set_new_data_in_wm(self.test_url, body=body)
            rpy = wm.call_mocked_service(self.test_url, request_body={"name": "Joe"})
            self.assertDictEqual(rpy.json(), expected_rpy_body)

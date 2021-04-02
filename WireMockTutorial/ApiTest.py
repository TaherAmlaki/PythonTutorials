import json

from WireMockTutorial.Utils import logger
from WireMockTutorial.Utils.WireMockContextManager import WireMockContext
from WireMockTutorial.Utils import WireMockCommunication


wiremock_jar_path = "docs/wiremock-standalone-2.27.2.jar"
root_path = "./wireMockRoot"
test_url = "/pythonTest"

with WireMockContext(wiremock_jar_path, root_path) as wm:
    wm.check_wiremock_running()
    wm.reset_mappings_and_requests_log()

    """ Let's put some simple stub which return Hello Multiverse for every request """
    WireMockCommunication.set_new_data_in_wm(test_url, body="Hello Multiverse!")

    rpy = WireMockCommunication.call_mocked_service(test_url)
    logger.info(rpy.content.decode("utf-8"))

    """ Now let's put a more complex response, where name property in request is used in response """
    body = {
        "message": "Hello {{jsonPath request.body '$.name'}}!"
    }
    WireMockCommunication.set_new_data_in_wm(test_url, body=body)
    rpy = WireMockCommunication.call_mocked_service(test_url, request_body={"name": "Taher"})
    logger.info(f"rpy => \n{json.dumps(rpy.json(), indent=4)}")

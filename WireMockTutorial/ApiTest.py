from WireMockTutorial.Utils.WireMockContextManager import WireMockContext


wiremock_jar_path = "./docs/wiremock-standalone-2.27.2.jar"
root_path = "./wireMockRoot"
with WireMockContext(wiremock_jar_path, root_path) as wm:
    wm.check_wiremock_running()
    wm.reset_mappings_and_requests_log()

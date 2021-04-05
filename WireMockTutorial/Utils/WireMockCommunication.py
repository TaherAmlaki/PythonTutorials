import requests
import json

from . import WireMockUrls, WireMockConnectionException, response_to_json, logger


class WireMockManager:
    @classmethod
    def set_new_data_in_wm(cls, url, headers=None, body=None,
                           method="POST", status_code=200):
        msg = {
            "request": {
                "method": method,
                "url": url
            },
            "response": {
                "status": int(status_code),
                "body": json.dumps(body, indent=4),
                "headers": headers
            }
        }
        msg = json.dumps(msg, indent=4)
        logger.debug(f"New response body to set in '{url}':\n{msg}")

        res = requests.post(WireMockUrls.MAPPINGS_URL, msg, headers={"Content-Type": "application/json"})
        if 400 <= res.status_code:
            raise WireMockConnectionException("Failed to set new data into WireMock: "
                                              f"{response_to_json(res)}")
        logger.info(f"Successfully set new data for {url}.")
        return res

    @classmethod
    def call_mocked_service(cls, url, request_body=None, request_headers=None,
                            method="POST", message_type="json"):
        url = WireMockUrls.WIREMOCK_URL + url
        if message_type == "json":
            request_body = json.dumps(request_body)
        return requests.request(method=method, url=url,
                                headers=request_headers, data=request_body)

    @classmethod
    def reset_mappings_and_requests_log(cls):
        res = requests.post(WireMockUrls.RESET_URL)
        return res.status_code < 400

    @classmethod
    def reset_mappings(cls):
        res = requests.post(WireMockUrls.MAPPINGS_RESET_URL)
        return res.status_code < 400

    @classmethod
    def shutdown_wiremock(cls):
        res = requests.post(WireMockUrls.SHUTDOWN_URL, data=None)
        if 400 <= res.status_code:
            raise WireMockConnectionException("Failed to shutdown WireMock Server.: "
                                              f"{response_to_json(res)}")
        logger.warning("WireMock Server was shutdown successfully.")

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


import requests

import json

from . import WireMockUrls, WireMockConnectionException, response_to_json


def set_new_data_in_wm(url, headers=None, body=None,
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
    res = requests.post(WireMockUrls.MAPPINGS_URL, msg, headers={"Content-Type": "application/json"})
    if 400 <= res.status_code:
        raise WireMockConnectionException("Failed to set new data into WireMock: "
                                          f"{response_to_json(res)}")
    return res


def call_mocked_service(url, request_body=None, request_headers=None,
                        method="POST", message_type="json"):
    url = WireMockUrls.WIREMOCK_URL + url
    if message_type == "json":
        request_body = json.dumps(request_body)
    return requests.request(method=method, url=url,
                            headers=request_headers, data=request_body)

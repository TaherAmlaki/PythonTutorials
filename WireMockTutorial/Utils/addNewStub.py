import requests

import json

from . import WIREMOCK_URL, WireMockConnectionException, response_to_json


def set_new_data_in_wm(url, headers=None, body=None, method="POST", status_code=200):
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
    print(msg)
    res = requests.post(f"{WIREMOCK_URL}/__admin/mappings", msg, headers={"Content-Type": "application/json"})
    if 400 <= res.status_code:
        raise WireMockConnectionException(f"Failed to set new data into WireMock: {response_to_json(res)}")
    return res

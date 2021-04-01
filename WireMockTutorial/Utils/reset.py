import requests

from . import WIREMOCK_URL


def reset_mappings(address=WIREMOCK_URL):
    res = requests.post(f"{address}/__admin/mappings/reset")
    return res.status_code < 400


# deprecated
def reset_requests_log(address=WIREMOCK_URL):
    res = requests.post(f"{address}/__admin/requests/reset")
    return res.status_code < 400


def reset_mappings_and_requests_log(address=WIREMOCK_URL):
    res = requests.post(f"{address}/__admin/reset")
    return res.status_code < 400

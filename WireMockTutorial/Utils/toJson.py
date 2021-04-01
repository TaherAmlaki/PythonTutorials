import json


def response_to_json(response):
    try:
        return json.dumps(response.json(), indent=4)
    except json.decoder.JSONDecodeError:
        return response.content.decode()
    except:
        raise TypeError("to_json got data which is not json serializable.")

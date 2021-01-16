from typing import Dict
import json


class DictToObj:
    def __init__(self, dictionary: Dict):
        self._dict = dictionary
        for key, value in dictionary.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [DictToObj(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, DictToObj(value) if isinstance(value, dict) else value)

    def to_dict(self):
        return self._dict

    def to_json(self, pretty=True):
        if pretty:
            return json.dumps(self._dict, ensure_ascii=True, indent=4)
        return json.dumps(self._dict, ensure_ascii=True)

    def items(self):
        for item_name, item_data in self._dict.items():
            yield item_name, DictToObj(item_data)

    def __repr__(self):
        return self.to_json()

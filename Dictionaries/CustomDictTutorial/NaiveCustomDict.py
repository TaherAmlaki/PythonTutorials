import re
import json


class StringKeyDict:
    def __init__(self, **kwargs):
        self._data = dict(**kwargs)

    def __setitem__(self, key, value):
        self._data[self.__convert_key(key)] = value

    def __getitem__(self, key):
        return self._data[self.__convert_key(key)]

    def __str__(self):
        return json.dumps(self._data, indent=4, ensure_ascii=True)

    @classmethod
    def __convert_key(cls, key):
        return re.sub(r'\W+', '_', str(key).strip())


d = StringKeyDict()
d[6] = "Six"
d["My Key"] = "My Value"
print(d)
"""
{
    "6": "Six",
    "My_Key": "My Value"
}
"""

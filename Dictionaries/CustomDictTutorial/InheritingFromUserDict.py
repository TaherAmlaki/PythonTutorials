import re
import json
from collections import UserDict


class StringKeyDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(self.__convert_key(key), value)

    def __getitem__(self, key):
        return super().__getitem__(self.__convert_key(key))

    def __str__(self):
        return json.dumps(self.data, indent=4, ensure_ascii=True)

    @classmethod
    def __convert_key(cls, key):
        return re.sub(r'\W+', '_', str(key).strip())


d = StringKeyDict()
d.update({"new key": "seven"})
print(d)
"""
{
    "new_key": "seven"
}

"""

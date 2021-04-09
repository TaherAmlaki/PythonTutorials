import json
import re


class StringKeyDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(self.__convert_key(key), value)
        
    def __getitem__(self, key):
        return super().__getitem__(self.__convert_key(key))

    def __str__(self):
        return json.dumps(self, indent=4, ensure_ascii=True)

    @classmethod
    def __convert_key(cls, key):
        return re.sub(r'\W+', '_', str(key).strip())


d = StringKeyDict(a="6", b="new key")
d.update({7: "seven"})
print(d)
"""
{
    "a": "6",
    "b": "new key",
    "7": "seven"
}
"""


import re


class StringKeyDict:
    def __init__(self):
        self._data = {}

    def __setitem__(self, key, value):
        self._data[self.__convert_key(key)] = value

    def __getitem__(self, key):
        return self._data[self.__convert_key(key)]

    @classmethod
    def __convert_key(cls, key):
        return re.sub(r'\W+', '_', str(key).strip())


d = StringKeyDict()
d[6] = "Six"
d["My Key"] = "My Value"
print(d._data)  # {'6': 'Six', 'My_Key': 'My Value'}

"""
We might start implementing a dictionary-like class to always convert keys to string
We can use bracket notation for setting and getting items, but we do not have get, update, pop, popitem, and 
views keys() and items()
available
"""

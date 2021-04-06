import re
from collections import UserDict


class StringKeyDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(self.__convert_key(key), value)

    def __getitem__(self, key):
        return super().__getitem__(self.__convert_key(key))

    @classmethod
    def __convert_key(cls, key):
        return re.sub(r'\W+', '_', str(key).strip())


d = StringKeyDict()
d[6] = "six"
d["My Key"] = "My Value"
print(d)  # {'6': 'six', 'My_Key': 'My Value'}

"""
We might start implementing a dictionary-like class to always convert keys to string
Inheriting from UserDict we can use bracket notation, all the views, and get and update work as expected.
"""
# d[6]=six, d.get(6)=six
print(f"d[6]={d[6]}, d.get(6)={d.get(6)}")

# {'6': 'six', 'My_Key': 'My Value', '7': 'seven'}
d.update({7: "seven"})
print(d)

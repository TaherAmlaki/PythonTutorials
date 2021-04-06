import re


class StringKeyDict(dict):
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
We can use bracket notation for setting and getting items and we have access to views keys and items, and get, update, 
pop, and popitem functionality but get and update are not using our underlying dictionary but rather just use 
C implementations
"""
# d[6]=six, d.get(6)=None, so get does not use __getitem__ and returns None because int 6 is not in dictionary
print(f"d['My Key']={d[6]}, d.get(6)={d.get(6)}")


# {'6': 'six', 'My_Key': 'My Value', 7: 'seven'}, update also does not use __setitem__
d.update({7: "seven"})
print(d)
print(d.pop(6))

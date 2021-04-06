from collections.abc import MutableMapping, Mapping
import re
import json


class DotDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.__data = kwargs
        self.update(**kwargs)

        for arg in args:
            self.__data[arg] = None
            setattr(self, arg, None)

    def __getitem__(self, key):
        return getattr(self, self.__convert_key(key))

    def __setattr__(self, prop: str, value):
        if prop == "_DotDict__data":
            super().__setattr__(prop, value)
        else:
            if isinstance(value, (list, tuple)):
                prop_obj = self.create_prop_obj_for_list_recursively(value)
            elif isinstance(value, Mapping):
                prop_obj = DotDict(**value)
            else:
                prop_obj = value
            super().__setattr__(prop, prop_obj)
            self.__data[prop] = value

    def __setitem__(self, key, value):
        setattr(self, self.__convert_key(key), value)

    def __delitem__(self, key):
        del self.__data[self.__convert_key(key)]
        del self.__dict__[self.__convert_key(key)]

    def __iter__(self):
        iterator = iter(self.__dict__)
        next(iterator)  # first key is _DotDict__data, so should not be in view
        return iterator

    def __len__(self):
        return len(self.__data)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        self.__data = {prop: self.call_to_dict_recursively(value) for prop, value in self.items()}
        return self.__data

    @classmethod
    def __convert_key(cls, key):
        key = re.sub(r'^\d+', '', str(key).lower()).strip()
        return re.sub(r'\W+', '_', key)

    @classmethod
    def create_prop_obj_for_list_recursively(cls, value):
        if isinstance(value, (list, tuple)):
            prop_obj = []
            for v in value:
                prop_obj.append(cls.create_prop_obj_for_list_recursively(v))
        elif isinstance(value, Mapping):
            prop_obj = DotDict(**value)
        else:
            prop_obj = value
        return prop_obj

    @classmethod
    def call_to_dict_recursively(cls, value):
        if isinstance(value, DotDict):
            return value.to_dict()
        elif isinstance(value, (list, tuple)):
            result = []
            for v in value:
                result.append(cls.call_to_dict_recursively(v))
            return result
        else:
            return value

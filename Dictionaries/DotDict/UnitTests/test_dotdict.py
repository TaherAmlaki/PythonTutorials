import json

import unittest

from Dictionaries.DotDict.DotDict import DotDict


class TestDotDictImplementation(unittest.TestCase):
    def test_dotdict_initialization(self):
        d = DotDict(b=21, c={"k1": "v1", "k2": "v2"})

        expected_dict = {'b': 21, 'c': {'k1': 'v1', 'k2': 'v2'}}
        self.assertDictEqual(d.to_dict(), expected_dict)

        expected_str = json.dumps(expected_dict, indent=4)
        self.assertEqual(str(d), expected_str)

        self.assertEqual(d.b, 21)
        self.assertEqual(d.c.k1, "v1")
        self.assertEqual(d.c.k2, "v2")

    def test_key_conversion_in_dotdict(self):
        d = DotDict(a={"k1": "v1", "k2": "v2"})
        d["Key With Space"] = "value"
        d["12 Key With Digits"] = "digits"
        self.assertTrue("Key_With_Space" in d)
        self.assertEqual(d.Key_With_Space, "value")
        self.assertTrue("Key_With_Digits" in d)
        self.assertEqual(d.Key_With_Digits, "digits")

    def test_assign_values_as_dict_list_dotdict(self):
        d = DotDict()
        d.dictionary = {"k1": "v1", "k2": "v2"}
        d.simple_list = ["L1", "L2"]
        d.dotdict = DotDict(dd1="vv1")

        self.assertEqual(d.dictionary.k2, "v2")
        self.assertEqual(d.simple_list[1], "L2")
        self.assertEqual(d.dotdict.dd1, "vv1")

        expected_dict = {'dictionary': {'k1': 'v1', 'k2': 'v2'},
                         'simple_list': ['L1', 'L2'],
                         'dotdict': {'dd1': 'vv1'}}
        expected_str = json.dumps(expected_dict, indent=4)
        self.assertEqual(str(d), expected_str)

    def test_nested_list_in_dotdict(self):
        d = DotDict()
        d.a = [
            "item1",
            {
                "item2": [
                    "nested_item_2",
                    {
                        "nested_item_3": "nested_item_3_value"
                    }
                ]
            }
        ]
        self.assertEqual(d.a[0], "item1")
        self.assertEqual(d.a[1].item2[0], "nested_item_2")
        self.assertEqual(d.a[1].item2[1].nested_item_3, "nested_item_3_value")

    def test_iteration_and_views(self):
        d = DotDict(**{'dictionary': {'k1': 'v1', 'k2': 'v2'},
                       'simple_list': ['L1', 'L2'],
                       'dotdict': {'dd1': 'vv1'}})
        expected_keys = ['dictionary', 'simple_list', 'dotdict']
        self.assertListEqual(list(d.keys()), expected_keys)

        iterator = iter(d)
        for key in expected_keys:
            self.assertEqual(key, next(iterator))

    def test_delete_item(self):
        d = DotDict(k2="value2")
        d.k3 = "value3"
        d.k4 = ["item4", {"item5": "value5"}, ["item6", {"item7": "value7"}]]

        del d["k2"]
        self.assertFalse("k2" in d)

        del d.k4[1].item5
        self.assertFalse("item5" in d.k4[1])

        del d.k4[2][1].item7
        expected_dict = {'k3': 'value3', 'k4': ['item4', {}, ['item6', {}]]}
        expected_str = json.dumps(expected_dict, indent=4)
        self.assertEqual(expected_str, str(d))

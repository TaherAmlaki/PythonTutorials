from collections import defaultdict


sentence = "The quick brown fox jumps over the lazy dog"

words_freq_map = {}
for word in sentence.split():
    if word not in words_freq_map:
        words_freq_map[word] = 1
    else:
        words_freq_map[word] += 1
print(words_freq_map)


# ========================================================
words_freq_map = {}
for word in sentence.split():
    words_freq_map[word] = words_freq_map.get(word, 0) + 1
print(words_freq_map)


# =========================================================
words_freq_map = defaultdict(lambda: 0)
for word in sentence.split():
    words_freq_map[word] += 1
print(words_freq_map)
print(words_freq_map["Eagle"])


# =========================================================
words_freq_map = defaultdict(int)
for word in sentence.split():
    words_freq_map[word] += 1
print(words_freq_map)
print(words_freq_map["Eagle"])


# =========================================================
from random import choice
import string

default_dict = defaultdict(lambda: {"random_value": choice(string.digits)})
for key in "ab":
    default_dict[key]["status"] = "ok"

print(default_dict)
# defaultdict(<function <lambda> at 0x000001B1AD927B80>,
# {'a': {'random_value': '5', 'status': 'ok'}, 'b': {'random_value': '0', 'status': 'ok'}})

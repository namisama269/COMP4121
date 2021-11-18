import random
import inflect
from statichashtable import StaticHashTable

"""
To test the static hash table, we will store a key as an integer from 0 to U
inclusive, and the key as the number in words.

inflect library is used to convert number to words: pip3 install inflect
"""

n = 15
U = 1000
infl = inflect.engine()
keys = list(random.sample(range(U+1), n))
values = [infl.number_to_words(key) for key in keys]

print(keys)
print()

ht = StaticHashTable(U, keys, values)

while True:
    try:
        key = int(input("Enter key to search: "))
        print(ht.search(key))
        print()
    except EOFError:
        break
"""
This is a test for the reading and writing of json files with emojis
I didn't know it worked so well so 5/5 for the huys who made this possible
"""
from json import load, dumps
from pprint import pprint

# dicti = {'a':"😀",'b':"😂"}

# with open('emojiDictionary.json', 'w+') as file:
#     file.write(dumps(dicti))

with open('emojiDictionary.json', 'r') as file:
    obj = load(file)

pprint(obj)
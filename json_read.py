import json
from pprint import pprint

json_file = open('trains.json')
data = json.load(json_file)
'''
for i in data:
    print(i)'''

print(data['train_p601']['path'][0]['0'])

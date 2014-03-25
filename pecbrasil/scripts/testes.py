import json
from pprint import pprint
json_data=open('network_hs.json')

data = json.load(json_data)

print "INICIO"
for song in data['edges']:   
    print "%s , %f , %s " % (data['nodes'][song['source']]['hs_id'],song['strength'],data['nodes'][song['target']]['hs_id'])
        
        
def printAll(data):
    for song in data['edges']:   
        print(song['source'])
        print(song['strength'])
        print(song['target'])
    
    for song in data['nodes']:   
        print(song['hs_id'])
        print(song['x'])
        print(song['y'])
print "FIM"
json_data.close()
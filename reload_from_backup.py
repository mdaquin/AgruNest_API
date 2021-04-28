import sys
import json
import requests

def create_doc(index, id, obj):    
    r=requests.put('http://localhost:9200/'+index+'/doc/'+id, json=obj)
    return json.loads(r.text)

if len(sys.argv) != 2:
    print("give file name")
    sys.exit(0)

with open(sys.argv[1]) as f:
    data = json.load(f)
    for item in data["hits"]["hits"]:
        id = item["_id"]
        index = item["_index"]
        print("adding "+id+" to "+index)
        d=create_doc(index, id, item["_source"])
        print(d)

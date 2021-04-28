from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import hashlib
import requests
from datetime import datetime
import urllib
import time

app = Flask('argunest_api')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

userkeys = {}

def get_doc(index, id):    
    r=requests.get('http://localhost:9200/'+index+'/_doc/'+id)
    return json.loads(r.text)

def create_doc(index, id, obj):    
    r=requests.put('http://localhost:9200/'+index+'/_doc/'+id, json=obj)
    return json.loads(r.text)

def delete_doc(index, id):    
    r=requests.delete('http://localhost:9200/'+index+'/_doc/'+id)
    return json.loads(r.text)

def search(index, query, size):
    r = ''
    if query == None:
        r=requests.get('http://localhost:9200/'+index+'/_search?size='+str(size))
    else:
        r=requests.get('http://localhost:9200/'+index+'/_search?size='+str(size)+'&q='+query)
    return json.loads(r.text)


def already_there(a,i):
    for j in a:
        if j["id"] == i:
            return True
    return False


def getRelations(aaid):
    query='origin:"'+aaid+'"'
    h = search('argunest_relations', query, 1000)
    result = {"supports": [], "contradicts": [], "same": []} 
    if 'hits' in h and 'hits' in h['hits']:
        for i in h['hits']['hits']:
            if "_source" in i:
                if i["_source"]["relation"] == "supports":
                    result["supports"].append(i["_source"]["target"])
                if i["_source"]["relation"] == "contradicts":
                    result["contradicts"].append(i["_source"]["target"])
                if i["_source"]["relation"] == "same":
                    result["same"].append(i["_source"]["target"])
    return result

@app.route('/graph', methods=['POST'])
@cross_origin()
def large_graph():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    print(data)    
    user = data["user"].encode('utf-8')
    doc = data["doc"]
    nodes = []
    r = search('argunest_users', 'email:'+user, 10)
    if "hits" in r and "hits" in r["hits"]:
        uid = r["hits"]["hits"][0]["_id"]        
        query = "user:"+uid+"+AND+doc:"+doc
        hits = search("argunest_annotations", query, 1000)
        if "hits" in hits and "hits" in hits["hits"]:
            for ann in hits["hits"]["hits"]:
                node = { 
                    "id": ann["_id"],
                    "label": ann["_source"]["title"],
                    "type": ann["_source"]["type"],
                    "linkto": ann["_source"]["topics"]
                }
                rels = getRelations(ann["_id"])
                node["supports"] = rels["supports"]
                node["contradicts"] = rels["contradicts"]
                node["same"] = rels["same"]        
                if not already_there(nodes, node["id"]):
                    nodes.append(node)
                for concept in ann["_source"]["topics"]:
                    if not already_there(nodes, concept):
                        nodet = { 
                            "id": concept,
                            "label": concept,
                            "type": "concept",
                            "linkto": []
                        }
                        nodes.append(nodet)
        response_obj = {"message": "graph created loaded", "nodes": nodes}
    else:
        response_obj = {'error': 'user not logged in'}        
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response

app.run(port=5002)

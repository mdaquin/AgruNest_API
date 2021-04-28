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

def new_key(uid, key):
    for k in userkeys:
        if "uid" in userkeys[k] and userkeys[k]["uid"] == uid:
            userkeys[k] = {"valid": False}
    userkeys[key] = {"uid": uid, "valid": True}
    print(userkeys)


@app.route('/log', methods=['POST'])
@cross_origin()
def log():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    key  = data["key"].encode('utf-8')
    mess = data["message"].encode('utf-8')
    par  = data["param"].encode('utf-8')
    if key in userkeys and "uid" in userkeys[key]:
        uid = userkeys[key]['uid']
        ltime=int(round(time.time() * 1000))
        lid = str(uid)+"-"+str(ltime)
        print("logged "+lid)
        lobj = {"id": lid, "uid": uid, "time": ltime, "message": mess, "param": par}
        r = create_doc("argunest_logs", lid, lobj)
    response_obj = {'OK': 'logged', 'id': lid}
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/text', methods=['POST'])
@cross_origin()
def load_text():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    key = data["key"].encode('utf-8')
    tid = data["id"].encode('utf-8')
    if key in userkeys and "uid" in userkeys[key]:
        d = get_doc('argunest_texts', tid)
        text = ''
        with open(d["_source"]["path"], 'r') as reader:
            text = reader.read()
        taxonomy = d["_source"]["taxonomy"]
        annotations = []
        query = "user:"+userkeys[key]["uid"]+"+AND+doc:"+tid
        hits = search("argunest_annotations", query, 1000)
        if "hits" in hits and "hits" in hits["hits"]:
            for ann in hits["hits"]["hits"]:
                annotations.append(ann["_source"])
        relations = {}
        query = "user:"+userkeys[key]["uid"]+"+AND+doc:"+tid
        hits = search("argunest_relations", query, 1000)
        if "hits" in hits and "hits" in hits["hits"]:
            for rels in hits["hits"]["hits"]:
                origin = rels["_source"]["origin"]
                relation = rels["_source"]["relation"]
                target = rels["_source"]["target"]
                if origin not in relations:
                    relations[origin] = {}
                if relation not in relations[origin]:
                    relations[origin][relation] = []
                relations[origin][relation].append(target)
        response_obj = {"message": "text loaded", "text": text, "annotations": annotations, "relations": relations, "taxonomy": taxonomy}
    else:
        response_obj = {'error': 'user not logged in'}        
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response


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

@app.route('/ann_graph', methods=['POST'])
@cross_origin()
def annotation_graph():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    key = data["key"].encode('utf-8')
    aid = data["id"].encode('utf-8')
    nodes = []
    if key in userkeys and "uid" in userkeys[key]:
        ann1 = get_doc('argunest_annotations', aid)
        # add link to other annotations
        node1 = { 
            "id": aid,
            "label": ann1["_source"]["title"],
            "type": ann1["_source"]["type"],
            "linkto": []
        }
        rels = getRelations(aid)
        node1["supports"] = rels["supports"]
        node1["contradicts"] = rels["contradicts"]
        node1["same"] = rels["same"]        
        nodes.append(node1)        
        for concept in ann1["_source"]["topics"]:
            if concept != "none":
                nodec = {
                    "id": concept,
                    "label": concept,
                    "type": "concept",
                    "linkto": []
                }
                if not already_there(nodes, concept):
                    nodes.append(nodec)
                node1["linkto"].append(concept)
                query = "topics:"+urllib.quote_plus(concept)+'+AND+user:'+userkeys[key]['uid']+'+AND+doc:'+ann1["_source"]["doc"]
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
        response_obj = {"message": "graph created loaded", "nodes": nodes}
    else:
        response_obj = {'error': 'user not logged in'}        
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/graph', methods=['POST'])
@cross_origin()
def large_graph():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    print(data)
    key = data["key"].encode('utf-8')
    doc = data["doc"]
    nodes = []
    if key in userkeys and "uid" in userkeys[key]:
        query = "user:"+userkeys[key]["uid"]+"+AND+doc:"+doc
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

@app.route('/annotation', methods=['POST'])
@cross_origin()
def add_annotation():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    key = data["user"].encode('utf-8')
    aid = data["id"].encode('utf-8')
    if key in userkeys and "uid" in userkeys[key]:
        uid = userkeys[key]["uid"]
        data["user"] = uid
        create_doc("argunest_annotations", aid, data)
        response_obj = {"message": "Annotation saved", "id": aid}     
    else:
        response_obj = {'error': 'user not logged in'}        
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/relation', methods=['POST'])
@cross_origin()
def add_relation():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    key    = data["key"].encode('utf-8')
    origin = data["origin"].encode('utf-8')
    rel    = data["relation"].encode('utf-8')
    target = data["target"].encode('utf-8')
    doc    = data["doc"].encode('utf-8')
    if key in userkeys and "uid" in userkeys[key]:
        uid = userkeys[key]["uid"]
        data["user"] = uid
        rid = hashlib.md5(data["user"].encode('utf-8')+
                          str(data["doc"])+
                          data["origin"]+
                          data["relation"]+
                          data["target"]).hexdigest()
        create_doc("argunest_relations", rid, data)
        response_obj = {"message": "Relation saved", "id": rid}     
    else:
        response_obj = {'error': 'user not logged in'}        
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/annotation/delete', methods=['POST'])
@cross_origin()
def delete_annotation():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    key = data["key"].encode('utf-8')
    aid = data["aid"].encode('utf-8')
    if key in userkeys and "uid" in userkeys[key]:
        uid = userkeys[key]["uid"]
        data["user"] = uid
        d = delete_doc("argunest_annotations", aid)
        print(d)
        response_obj = {"message": "Annotation deleted", "id": aid}     
    else:
        response_obj = {'error': 'user not logged in'}        
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/relation/delete', methods=['POST'])
@cross_origin()
def delete_relation():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    key = data["key"].encode('utf-8')
    key    = data["key"].encode('utf-8')
    origin = data["origin"].encode('utf-8')
    rel    = data["relation"].encode('utf-8')
    target = data["target"].encode('utf-8')
    doc    = data["doc"].encode('utf-8')
    if key in userkeys and "uid" in userkeys[key]:
        uid = userkeys[key]["uid"]
        data["user"] = uid
        rid = hashlib.md5(data["user"].encode('utf-8')+
                          str(data["doc"])+
                          data["origin"]+
                          data["relation"]+
                          data["target"]).hexdigest()        
        d = delete_doc("argunest_relations", rid)
        print(d)
        response_obj = {"message": "Relation deleted", "id": rid}     
    else:
        response_obj = {'error': 'user not logged in'}        
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/texts', methods=['POST'])
@cross_origin()
def list_texts():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    key = data["key"].encode('utf-8')
    if key in userkeys and "uid" in userkeys[key]:
        fes = search("argunest_texts", None, 100)
        result = {"message": "list of texts retrieved", "list": []}
        if "hits" in fes and "hits" in fes["hits"]:
            for o in fes["hits"]["hits"]:
                nr ={"id": o["_id"], "title": o["_source"]["title"]}
                result["list"].append(nr)
            response_obj = result
        else:
            response_obj = {'error': 'could not get list of text'}
    else:
        response_obj = {'error': 'user not logged in'}        
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response
    
@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    uid = hashlib.md5(data["email"].encode('utf-8')).hexdigest()
    d = get_doc('argunest_users', uid)
    if not d["found"]:
        obj={'email': data["email"], 'password':hashlib.sha1(data["password"].encode('utf-8')).hexdigest()}
        d = create_doc('argunest_users', uid, obj)
        print("=== user created: ===")
        print(d)
        response_obj = {'message': 'user created, you should be able to login now'}
    else:
        response_obj = {'error': 'user already exists!'}
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    response_obj = {'error': 'something wrong happened'}
    data = request.get_json(silent=True)
    uid = hashlib.md5(data["email"].encode('utf-8')).hexdigest()
    d = get_doc('argunest_users', uid)
    if not d["found"]:
        response_obj = {'error': 'user or password incorrect'}
    else:        
        passwd1 = hashlib.sha1(data["password"].encode('utf-8')).hexdigest()
        passwd2 = d["_source"]["password"]
        if passwd1 == passwd2:
            response_obj = {
                'message': 'Welcome to ArguNest!',
                'key': hashlib.md5(str(datetime.now().microsecond)).hexdigest()}
            new_key(uid,response_obj['key'])
        else:
            response_obj = {'error': 'user or password incorrect'}            
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response

app.run()

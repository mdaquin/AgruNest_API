from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import hashlib
import requests
from datetime import datetime

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
        response_obj = {"message": "text loaded", "text": text}        
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

from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import hashlib
import requests

app = Flask('argunest_api')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_doc(index, id):    
    r=requests.get('http://localhost:9200/'+index+'/_doc/'+id)
    return json.loads(r.text)

def create_doc(index, id, obj):    
    r=requests.put('http://localhost:9200/'+index+'/_doc/'+id, json=obj)
    return json.loads(r.text)

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
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
        
    # id is hash of email
    # get it 
    # check if we already know a
    # data["email"]
    # if not add the doc...
    response = app.response_class(
        response=json.dumps(response_obj),
        status=200,
        mimetype='application/json'
    )
    return response

app.run()

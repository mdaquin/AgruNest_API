import requests
import json
import datetime

def search(index, query, size):
    r = ''
    if query == None:
        r=requests.get('http://localhost:9200/'+index+'/_search?size='+str(size))
    else:
        r=requests.get('http://localhost:9200/'+index+'/_search?size='+str(size)+'&q='+query)
    return json.loads(r.text)


users = {}

r = search("argunest_users", None, 100)
for hit in r["hits"]["hits"]:
    users[hit["_id"]] = hit["_source"]["email"]

data = {}

for user in users:
    u = users[user]
    data[u] = {}
    r = search("argunest_logs", "uid:"+user, 2000)
    nbi = r["hits"]["total"]["value"]    
    data[u]["nbi"] = nbi
    maxt = 0
    mint = 2980052997792
    for hit in r["hits"]["hits"]:
        if hit["_source"]["time"] > maxt:
            maxt = hit["_source"]["time"]
        if hit["_source"]["time"] < mint:
            mint = hit["_source"]["time"]
    data[u]["mint"] = datetime.datetime.fromtimestamp(mint/1000)
    data[u]["maxt"] = datetime.datetime.fromtimestamp(maxt/1000)
    r = search("argunest_annotations", "user:"+user, 2000)
    data[u]["nba"] = r["hits"]["total"]["value"]
    count = 0
    for hit in r["hits"]["hits"]:
        if hit["_source"]["doc"] == '22':
            count = count + 1
    data[u]["nba22"] = count
    r = search("argunest_relations", "user:"+user, 2000)    
    data[u]["nbr"] = r["hits"]["total"]["value"]
    count = 0
    for hit in r["hits"]["hits"]:
        if hit["_source"]["doc"] == '22':
            count = count + 1
    data[u]["nbr22"] = count
    
print ("user, nb actions, first action, last action, nb annotations, nb relations, nb annotations in text 22, nb relations in text 22")
for u in data:
    if data[u]["nbi"] > 0:
        print (u+","+str(data[u]["nbi"])+","+str(data[u]["mint"])+","+str(data[u]["maxt"])+","+str(data[u]["nba"])+","+str(data[u]["nbr"])+","+str(data[u]["nba22"])+","+str(data[u]["nbr22"]))


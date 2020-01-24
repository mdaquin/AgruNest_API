import hashlib
import requests
import math
import re
import json
import os
import sys

wdtermcache = {}
caches = []
countcache = {}
N = 0

path = 'cache2/'
files = []
for r, d, f in os.walk(path):
    for file in f:
        files.append(int(file))
        print(file)

files.sort()
for cf in files:
    with open('cache2/'+str(cf)) as f:
        caches.append(json.load(f))

def getcount(t):
    for cache in caches:
        if t in cache:
            return cache[t]        
    r = requests.get('http://localhost:9200/dbpedia_abstracts/_count?q='+t)
    caches[len(caches)-1][t] = r.json()["count"]
    with open('cache2/'+str(len(caches)-1), 'w') as outfile:
        json.dump(caches[len(caches)-1], outfile)
    if len(caches[len(caches)-1]) > 50000:
        caches.append({})
    return r.json()["count"]


def load_text(wd_id, toassess):
    response_obj = {}
    #data = request.get_json(silent=True)
    #wd_id = data["id"].encode('utf-8')
    #toassess  = data["text"].encode('utf-8')
    uri = 'http://wikidata.dbpedia.org/resource/'+wd_id
    id = hashlib.md5(uri).hexdigest()
    r = requests.get('http://localhost:9200/dbpedia_abstracts/_count')
    N=r.json()['count']
    if uri not in wdtermcache:
        r = requests.get('http://localhost:9200/dbpedia_abstracts/_termvectors/'+id)
        terms = []
        vect = r.json()["term_vectors"]["text"]["terms"]
        for term in vect:
            nterm = re.sub('[^A-Za-z]', '', term.lower())
            freq = vect[term]["term_freq"]
            nfreq = math.log(1+freq) # log normalisation
            docfreq = getcount(nterm)
            idf = 0
            if docfreq != 0:
                idf = math.log(N/docfreq)
            terms.append({
                "term": nterm,
                "N": N,
                "freq": freq,
                "nfreq": nfreq,
                "docfreq": docfreq,
                "idf": idf,
                "tfidf": nfreq*idf
            })
        wdtermcache[uri] = terms
    terms = wdtermcache[uri]
    atoassess = toassess.split()
    rterms = []
    for word in atoassess:
        cword = re.sub('[^A-Za-z]', '', word.lower())
        if cword not in rterms:
            rterms.append(cword)
    for term1 in rterms:
        D1 = getcount(term1)
        sumt1 = 0
        sumws = 0
        for term2 in terms:
            if term1 != "" and term2["term"] != "":
                D12 = getcount(term1+" AND "+term2["term"])
                D2 = term2["docfreq"]
                # print(str(D1)+" "+str(D2)+" "+str(D12))
                DEN = (float(D1)*(float(D2)))/float(N)
                if D12 != 0:
                    PMI = (float(D12)/float(N))/DEN
                else:
                    PMI = 0
                sumt1 = sumt1 + term2["tfidf"]*PMI
                sumws = sumws + term2["tfidf"]
                # print(term1+" "+term2["term"]+" "+str(PMI))
        if term1 != "":
            print(term1+" "+str(sumt1*10000/sumws))
            response_obj[term1] = sumt1*10000/sumws
    return response_obj

# app.run(port=5001)

# load text version of excerpts
# get id from params
# run

text = ""
with open('texts/e-r.txt', 'r') as file:
    text = file.read()

qid = sys.argv[1]

load_text(qid, text)


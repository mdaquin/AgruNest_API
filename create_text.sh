curl -X POST "http://localhost:9200/argunest_texts/_doc/11" -H 'Content-Type: application/json' -d'
{
    "path": "texts/existantial-comic-242.txt", 
    "title": "Existantial comic 242",
    "taxonomy": [
       {"label": "Human", "dbp_uri": "http://dbpedia.org/resource/Human", "wdid": "Q5"},
       {"label": "Animal", "dbp_uri": "http://dbpedia.org/resource/Animal", "wdid": "Q729"},
       {"label": "Reason", "dbp_uri": "http://dbpedia.org/resource/Reason", "wdid": "Q178354"},
       {"label": "Instinct", "dbp_uri": "http://dbpedia.org/resource/Instinct", "wdid": "Q18237"},
       {"label": "Language", "dbp_uri": "http://dbpedia.org/resource/Language", "wdid": "Q315"},
       {"label": "Thought", "dbp_uri": "http://dbpedia.org/resource/Thought", "wdid": "Q9420"},
       {"label": "Soul ", "dbp_uri": "http://dbpedia.org/resource/Soul", "wdid": "Q9165"},
       {"label": "Experience", "dbp_uri": "http://dbpedia.org/resource/Experience", "wdid": "Q164359"},
       {"label": "Feeling", "dbp_uri": "http://dbpedia.org/resource/Feeling", "wdid": "Q205555"},
       {"label": "Pain", "dbp_uri": "http://dbpedia.org/resource/Pain_(philosophy)", "wdid": "Q4358242"},
       {"label": "Will", "dbp_uri": "http://dbpedia.org/resource/Will_(philosophy)", "wdid": "Q364340"},
       {"label": "Promise", "dbp_uri": "http://dbpedia.org/resource/Promise", "wdid": "Q1425577"},
       {"label": "Understanding", "dbp_uri": "http://dbpedia.org/resource/Understanding", "wdid": "Q46744"},
       {"label": "Sadness", "dbp_uri": "http://dbpedia.org/resource/Sadness", "wdid": "Q169251"}
     ]
}'

curl -X POST "http://localhost:9200/argunest_texts/_doc/22" -H 'Content-Type: application/json' -d'
{
    "path": "texts/excerpts.txt", 
    "title": "Excerpts from Early Modern Theophilosophical Texts",
    "taxonomy": [
       {"label": "Charity", "dbp_uri": "http://dbpedia.org/resource/Charity_(virtue)", "wdid": "Q456673"},
       {"label": "Cause", "dbp_uri": "http://dbpedia.org/resource/Four_causes", "wdid": "Q3140529"},
       {"label": "Occasionalism", "dbp_uri": "http://dbpedia.org/resource/Occasionalism", "wdid": "Q651345"},
       {"label": "Desire ", "dbp_uri": "http://dbpedia.org/resource/Desire", "wdid": "Q775842"},
       {"label": "God ", "dbp_uri": "http://dbpedia.org/resource/God", "wdid": "Q190"},
       {"label": "Love ", "dbp_uri": "http://dbpedia.org/resource/Love", "wdid": "Q316"},
       {"label": "Love of God", "dbp_uri": "http://dbpedia.org/resource/Love_of_God", "wdid": "Q967441"},
       {"label": "Pain ", "dbp_uri": "http://dbpedia.org/resource/Pain_(philosophy)", "wdid": "Q4358242"},
       {"label": "Pleasure ", "dbp_uri": "http://dbpedia.org/resource/Pleasure#Philosophies_of_pleasure", "wdid": "Q208195"},
       {"label": "Sensation ", "dbp_uri": "http://dbpedia.org/resource/Sensation_(psychology)", "wdid": "Q3955369"},
       {"label": "Soul ", "dbp_uri": "http://dbpedia.org/resource/Soul", "wdid": "Q9165"},
       {"label": "Will of God ", "dbp_uri": "http://dbpedia.org/resource/Will_of_God", "wdid": "Q8003236"},
       {"label": "Sociability", "dbp_uri": "http://dbpedia.org/resource/Sociality", "wdid": "Q3307505"},
       {"label": "Object", "dbp_uri": "http://dbpedia.org/resource/Object_(philosophy)", "wdid": "Q488383"}
    ]
}'







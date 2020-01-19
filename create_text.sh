curl -X POST "http://localhost:9200/argunest_texts/_doc/1" -H 'Content-Type: application/json' -d'
{
    "path": "texts/existantial-comic-242.txt", 
    "title": "Existantial comic 242"
}'

curl -X POST "http://localhost:9200/argunest_texts/_doc/2" -H 'Content-Type: application/json' -d'
{
    "path": "texts/excerpts_1.txt", 
    "title": "Excerpts from Early Modern Theophilosophical Texts I"
}'

curl -X POST "http://localhost:9200/argunest_texts/_doc/3" -H 'Content-Type: application/json' -d'
{
    "path": "texts/excerpts_2.txt", 
    "title": "Excerpts from Early Modern Theophilosophical Texts II"
}'

curl -X POST "http://localhost:9200/argunest_texts/_doc/4" -H 'Content-Type: application/json' -d'
{
    "path": "texts/excerpts_3.txt", 
    "title": "Excerpts from Early Modern Theophilosophical Texts III"
}'






curl -X GET "localhost:9200/argunest_annotations/_search?size=0&pretty" -H 'Content-Type: application/json' -d'
{
    "aggs" : {
        "uids" : {
            "terms" : { "field" : "user.keyword", "size": 50} 
        }
    }
}
'  | grep 'key\|"doc_count"'

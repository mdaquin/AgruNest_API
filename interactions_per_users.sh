curl -X GET "localhost:9200/argunest_logs/_search?size=0&pretty" -H 'Content-Type: application/json' -d'
{
    "aggs" : {
        "uids" : {
            "terms" : { "field" : "uid.keyword", "size":50}
        }
    }
}
'  | grep 'key\|"doc_count"'

sleep 60
curl localhost:8080/alter?runInBackground=true -XPOST -d '
    name: string @index(fulltext) .
    knows: [uid] @reverse .
'
sleep 20
curl -H "Content-Type: application/json" localhost:8080/mutate?commitNow=true -XPOST -d '{"set": [{"name": "Carlos","uid": "0x1","knows": [{"name": "Ana","uid": "0x2","knows": [{"name": "Maria","uid": "0x3","knows": [{"name": "Vinicius","uid": "0x4","knows": [{"uid": "0x2"}]}]},{"name": "João","uid": "0x5","knows": [{"name": "Luiza","uid": "0x6"}]}]}]}]}'

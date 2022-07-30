
GET /_cat/indices?v

GET recipe_db/_search

DELETE recipe_db

GET recipe_db/_search
{
  "query": {
    "match": {
      "ingredients_nm": ""
    }
  }
}

POST recipe_db/_delete_by_query
{
  "query": { 
    "match": {
      "recipe_nm": ""
    }
  }
}
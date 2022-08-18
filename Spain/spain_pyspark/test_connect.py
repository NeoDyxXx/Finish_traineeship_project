from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(
    cloud_id='hello:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDQxZDRkZmZlYWNiYTQ4MGJhNWY2OTAwYmJhYzYwMWE1JGY0ZjM2NzU5NjFkNDRlNjE5MGQwYzZlYzYwYTgwYTRj',
    basic_auth=('elastic', 'RNwz2XcJGWZgKhWhqBB9w8Bn')
)

print(es.info())
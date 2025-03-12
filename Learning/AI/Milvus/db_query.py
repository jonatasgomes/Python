from pymilvus import connections, Collection, utility

connections.connect(
  alias="milvus_conn", host="localhost", port="19530", db_name="linkedin_db"
)
courses_collection = Collection(name="courses_list", using="milvus_conn")
courses_collection.load()

result = courses_collection.query(
  expr='course_id == 1001',
  output_fields=['title', 'description'],
)
print(result)
result = courses_collection.query(
  expr='title like "MLOps%" && course_id > 1001',
  output_fields=['title', 'description'],
)
print(result)

connections.disconnect(alias="milvus_conn")

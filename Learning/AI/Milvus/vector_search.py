from pymilvus import connections, Collection
from langchain_openai import OpenAIEmbeddings
import env

connections.connect(
  alias="milvus_conn", host="localhost", port="19530", db_name="linkedin_db"
)
courses_collection = Collection(name="courses_list", using="milvus_conn")
courses_collection.load()

embeddings_model = OpenAIEmbeddings(api_key=env.OPENAI_API_KEY)
search_embed = embeddings_model.embed_query('machine learning')

search_params = {
  "metric_type": "L2",
  "offset": 0,
  "ignore_growing": False,
  "params": {"nprobe": 10}
}
results = courses_collection.search(
  data=[search_embed],
  anns_field="desc_embedding",
  param=search_params,
  limit=10,
  expr=None,
  output_fields=["title"],
  consistency_level="Strong"
)
# print(type(results[0]))
for i in results[0]:
  print(i.id, str(round(i.distance, 2)), '\t', i.entity.get("title"))

connections.disconnect(alias="milvus_conn")

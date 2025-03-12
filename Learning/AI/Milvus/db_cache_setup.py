from pymilvus import connections, db
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType
import json

cache_db_name = 'cache_db'
cache_collection_name = 'llm_cache'
conn_alias = "milvus_conn"
connections.connect(
  alias=conn_alias, host="localhost", port="19530"
)
current_dbs = db.list_database(conn_alias)
print(current_dbs)
if cache_db_name not in current_dbs:
  db.create_database(cache_db_name, using=conn_alias)
  print('Database created.')
else:
  print('Database cache already exists.')
db.using_database(cache_db_name, using=conn_alias)

cache_id = FieldSchema(
  name='cache_id',
  dtype=DataType.INT64,
  auto_id=True,
  is_primary=True,
  max_length=32
)

prompt_text = FieldSchema(
  name='prompt_text',
  dtype=DataType.VARCHAR,
  max_length=2048
)

response_text = FieldSchema(
  name='response_text',
  dtype=DataType.VARCHAR,
  max_length=2048
)

prompt_embedding = FieldSchema(
  name='prompt_embedding',
  dtype=DataType.FLOAT_VECTOR,
  dim=1536
)

cache_schema = CollectionSchema(
  fields=[cache_id, prompt_text, response_text, prompt_embedding],
  description='Cache for LLM',
  enable_dynamic_field=True
)

cache_collection = Collection(
  name=cache_collection_name,
  schema=cache_schema,
  using=conn_alias,
  shard_num=2
)
print('Schema ', cache_collection.schema)

index_params = {
  "metric_type": "L2",
  "index_type": "IVF_FLAT",
  "params": {"nlist": 1024},
}

cache_collection.create_index(
  field_name='prompt_embedding',
  index_params=index_params
)
cache_collection.flush()
cache_collection.load()

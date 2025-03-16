from pymilvus import connections, db, Collection
from pymilvus import FieldSchema, CollectionSchema, DataType

db_name = 'rag_db'
conn_alias = 'rag_con'
connections.connect(alias=conn_alias, host="localhost", port="19530")

current_dbs = db.list_database(using=conn_alias)
if (db_name not in current_dbs):
  db.create_database(db_name=db_name, using=conn_alias)
  print(f'Database {db_name} created.')
db.using_database(db_name=db_name, using=conn_alias)

chunk_id_field = FieldSchema(
  name='chunk_id',
  dtype=DataType.INT64,
  is_primary=True,
  max_length=32
)
rag_text_field = FieldSchema(
  name='rag_text',
  dtype=DataType.VARCHAR,
  max_length=2048
)
rag_embedding_field = FieldSchema(
  name='rag_embedding',
  dtype=DataType.FLOAT_VECTOR,
  dim=1536
)

rag_schema = CollectionSchema(
  fields=[chunk_id_field, rag_text_field, rag_embedding_field],
  description='RAG Schema',
  enable_dynamic_field=True
)
rag_col = Collection('rag_collection', schema=rag_schema, using=conn_alias, shard_num=2)
print(f'Collection {rag_col.name} created.')

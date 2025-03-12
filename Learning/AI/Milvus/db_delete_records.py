from pymilvus import connections, Collection, utility

conn_alias = 'milvus_conn'
connections.connect(
  alias=conn_alias, host="localhost", port="19530", db_name='cache_db'
)
cache_collection = Collection(
  name='llm_cache',
  using=conn_alias,
)

# Delete all records for the collection
cache_collection.load()  # Load the collection into memory
delete_expr = "0 == 0"  # Expression to match all entities
result = cache_collection.delete(delete_expr)

print(f"Deleted {result.delete_count} entities from the collection.")

# Optional: Compact the collection to reclaim disk space
cache_collection.compact()

# Release the collection from memory
cache_collection.release()

# Optionally, you can flush the collection to ensure changes are persisted
utility.flush([cache_collection.name])

print("All records have been deleted from the collection.")

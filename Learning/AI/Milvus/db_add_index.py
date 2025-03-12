from pymilvus import connections, Collection, utility

connections.connect(
    alias="milvus_conn", host="localhost", port="19530", db_name="linkedin_db"
)
courses_collection = Collection(name="courses_list", using="milvus_conn")
courses_collection.create_index(
    field_name="desc_embedding",
    index_params={
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 2048},
    },
)
print(utility.index_building_progress(collection_name="courses_list", using="milvus_conn"))
connections.disconnect(alias="milvus_conn")

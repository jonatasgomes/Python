import pandas as pd
from langchain_openai import OpenAIEmbeddings
from pymilvus import connections, Collection
import os
import env

path = os.getcwd() + '/Setup/course-descriptions.csv'
data = pd.read_csv(path)
course_id = data['Course ID'].tolist()
title = data['Title'].tolist()
description = data['Description'].tolist()

embeddings_model = OpenAIEmbeddings(api_key=env.OPENAI_API_KEY)
desc_embedding = [embeddings_model.embed_query(i) for i in description]
insert_data = [course_id, title, description, desc_embedding]

connections.connect(alias="milvus_conn", host="localhost", port="19530", db_name="linkedin_db")
courses_collection = Collection(name="courses_list", using="milvus_conn")
courses_collection.insert(insert_data)
courses_collection.flush(timeout=180)
print("Data loaded successfully.")
connections.disconnect(alias="milvus_conn")

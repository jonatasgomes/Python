from pymilvus import connections, Collection, utility
from langchain_community.document_loaders import PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import os, env

conn_alias = 'rag_con'
connections.connect(alias=conn_alias, host='localhost', port='19530', db_name='rag_db')
rag_col = Collection('rag_collection', using=conn_alias)
print(f'Collection {rag_col.name} loaded.')

load_path = os.path.join(os.path.dirname(__file__), 'Setup/Large Language Models.pdf')
loader = PDFMinerLoader(load_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=512,
  chunk_overlap=32,
  length_function=len
)
docs = text_splitter.split_documents(docs)
rag_text = []
for i in docs:
  rag_text.append(i.page_content)
# print(f'Chunks: {len(rag_text)}\nSample chunk: {rag_text[1]}')

ebd_model = OpenAIEmbeddings(api_key=env.OPENAI_API_KEY)
rag_ebd = [ebd_model.embed_query(i) for i in rag_text]
ebd_ids = [i for i in range(len(rag_text))]
insert_data = [ebd_ids, rag_text, rag_ebd]
rag_col.insert(insert_data)
rag_col.flush()

index_params = {
  'metric_type': 'L2',
  'index_type': 'IVF_FLAT',
  'params': { 'nlist': 1024 }
}
rag_col.create_index(
  field_name='rag_embedding',
  index_params=index_params
)
idx = utility.index_building_progress(rag_col.name, using=conn_alias)
print(idx)

from pymilvus import connections, Collection
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
import env

conn_alias = 'rag_con'
connections.connect(alias=conn_alias, host='localhost', port='19530', db_name='rag_db')
rag_col = Collection('rag_collection', using=conn_alias)
rag_col.load()
# print(f'Collection {rag_col.name} loaded.')

ebd_model = OpenAIEmbeddings(api_key=env.OPENAI_API_KEY)
query = 'How can I decrease gender bias in LLM and what would be the benefits?'
query_ebd = ebd_model.embed_query(query)
search_params = {
  'metric_type': 'L2',
  'offset': 0,
  'ignore_growing': False,
  'params': { 'nprobe': 20, 'radius': 0.5 }
}
results = rag_col.search(
  data=[query_ebd],
  anns_field='rag_embedding',
  param=search_params,
  limit=3,
  expr=None,
  output_fields=['rag_text'],
  consistency_level='Strong'
)
# print(f'Top result: {results[0][0]}')

context = []
for i in range(len(results[0])):
  context.append(results[0][i].entity.get('rag_text'))
prompt = (
  f'Based on only the provided context answer the query below:\n'
  f'Context: {context}\n\n'
  f'Query: {query}'
)
# print(prompt)

llm = OpenAI(api_key=env.OPENAI_API_KEY)
answer = llm.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ],
  temperature=0.0
)
print(answer.choices[0].message.content)

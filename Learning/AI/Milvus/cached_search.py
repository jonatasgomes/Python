from pymilvus import connections, Collection
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # Changed import
import env
import time

conn_alias = 'milvus_conn'
connections.connect(
    alias=conn_alias, 
    host="localhost", 
    port="19530", 
    db_name='cache_db'
)

cache_collection = Collection(
    name='llm_cache',
    using=conn_alias,
)

# FIX 1: Use ChatOpenAI instead of OpenAI for chat models
llm = ChatOpenAI(  # Changed class
    temperature=0.0,
    model='gpt-3.5-turbo',  # Correct model name
    api_key=env.OPENAI_API_KEY,
)

# FIX 2: Separate embeddings model remains correct
embeddings_model = OpenAIEmbeddings(
    model='text-embedding-ada-002',
    api_key=env.OPENAI_API_KEY
)

similarity_threshold = 0.3
search_params = {
    'metric_type': 'L2',
    'offset': 0,
    'ignore_growing': False,
    'params': {'nprobe': 20, 'radius': similarity_threshold}
}

def get_response(prompt):
    start_time = time.time()
    prompt_embed = embeddings_model.embed_query(prompt)
    
    # Milvus search remains unchanged
    cache_results = cache_collection.search(
        data=[prompt_embed],
        anns_field='prompt_embedding',
        param=search_params,
        limit=1,
        expr=None,
        output_fields=['prompt_text', 'response_text'],
        consistency_level='Strong'
    )
    
    returned_response = 'None'
    if len(cache_results[0]) > 0:
        print(prompt, ':\nCache hit: ', cache_results[0])
        returned_response = cache_results[0][0].entity.get('response_text')
    else:
        # FIX 3: Proper chat model invocation
        llm_response = llm.invoke([
            {"role": "user", "content": prompt}  # Correct message format
        ]).content
        
        print(prompt, ':\nLLM returned:', llm_response)
        
        # Insert to cache remains unchanged
        prompt_text = [prompt]
        prompt_embedding = [prompt_embed]
        response_text = [llm_response]
        insert_data = [prompt_text, response_text, prompt_embedding]
        cache_collection.insert(insert_data)
    
    end_time = time.time()
    print('Time elapsed:', end_time - start_time)
    return returned_response

# Test queries
get_response('When was Abraham Lincoln born?')
get_response('What are the advantages of Python language?')
get_response('What is the typical height of an elephant?')
get_response('List some advantages of Python language')

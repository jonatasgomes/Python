from langchain_huggingface import HuggingFaceEndpoint
import env

llm = HuggingFaceEndpoint(
  repo_id='tiiuae/falcon-7b-instruct',
  huggingfacehub_api_token=env.HF_ACCESS_TOKEN
)

question = 'Can you still have fun'
output = llm.invoke(question)
print(output)

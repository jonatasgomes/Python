from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
import env

template = "You're an AI assistant, answer the question. {question}"
prompt_template = PromptTemplate(template=template, input_variables=['question'])
llm = HuggingFaceEndpoint(repo_id='tiiuae/falcon-7b-instruct', huggingfacehub_api_token=env.HF_ACCESS_TOKEN)
llm_chain = prompt_template | llm
question = 'What is LangChain?'
print(llm_chain.invoke({ 'question': question}))

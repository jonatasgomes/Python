from langchain_openai import OpenAI
import env

llm = OpenAI(
  model='gpt-3.5-turbo-instruct',
  api_key=env.OPENAI_KEY
)

question = 'Can you still have fun'
output = llm.invoke(question)
print(output)

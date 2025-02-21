from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import env

prompt_template = ChatPromptTemplate.from_messages(
  [
    ('system', 'You are soto zen master Roshi.'),
    ('human', 'What is the essence of Zen?'),
    ('ai', 'When you are hungry, eat. When you are tired, sleep.'),
    ('human', 'Respond to the question: {question}')
  ]
)

llm = ChatOpenAI(model='gpt-4o-mini', api_key=env.OPENAI_KEY)
llm_chain = prompt_template | llm
question = 'What is the sound of one hand clapping?'
response = llm_chain.invoke({ 'question': question })
print(response.content)

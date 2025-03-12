from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
import env

examples = [
  {
    "question": "How many DataCamp courses has Jack completed?",
    "answer": "36"
  },
  {
    "question": "How much XP does Jack have on DataCamp?",
    "answer": "284,320XP"
  },
  {
    "question": "What technology does Jack learn about most on DataCamp?",
    "answer": "Python"
  }
]
example_prompt = PromptTemplate.from_template("Question: {question}\n{answer}")
prompt_template = FewShotPromptTemplate(
  examples=examples,
  example_prompt=example_prompt,
  suffix='Question: {input}',
  input_variables=['input'],
)

llm = ChatOpenAI(model='gpt-3.5-turbo', api_key=env.OPENAI_KEY)
llm_chain = prompt_template | llm
print(llm_chain.invoke({'input': 'What is Jack\'s favorite programming language?'}))

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

prompt_template = PromptTemplate.from_template(
    "Create a travel itinerary for {destination} for {number_of_days} days, including activities and places to visit."
)
prompt = prompt_template.format(
    destination="Mississauga, Ontario, Canada",
    number_of_days=5
)

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)
resp = llm.invoke(prompt)

print(resp.content)

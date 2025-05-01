from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.globals import set_debug
import os

set_debug(True)
city_template = ChatPromptTemplate.from_template(
    "Suggest a destination given my interest in {interest}. The output should be ONLY a city name. City: "
)
restaurants_template = ChatPromptTemplate.from_template(
    "Suggest popular restaurants amongst locals in {city}"
)
cultural_activities_template = ChatPromptTemplate.from_template(
    "Suggest cultural activities in {city}"
)

openai_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

chain = city_template | openai_llm | restaurants_template | openai_llm | cultural_activities_template | openai_llm
response = chain.invoke({"interest": "dating"})
print(response.content)

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.globals import set_debug
from operator import itemgetter
import os


class Destination(BaseModel):
    city: str = Field(description="Destination to visit")
    purpose: str = Field(description="Purpose of the trip")
    interest: str = Field(description="Interest of the user")

set_debug(True)
json_parser = JsonOutputParser(pydantic_object=Destination)

city_template = PromptTemplate(
    template="Suggest a destination given my interest in {interest}.\n\n{output_format}",
    input_variables=["interest"],
    partial_variables={"output_format": json_parser.get_format_instructions()},
)
restaurants_template = ChatPromptTemplate.from_template(
    "Suggest popular restaurants amongst locals in {city}"
)
cultural_activities_template = ChatPromptTemplate.from_template(
    "Suggest cultural activities in {city}"
)
response_template = ChatPromptTemplate.from_messages([
    ("ai", "Based on your interest in {interest}, I suggest visiting {city}."),
    ("ai", "Here are some popular restaurants: {restaurants}."),
    ("ai", "And here are some cultural activities: {activities}."),
    ("system", "Combine the responses into 2 coherent paragraphs."),
])

openai_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

chain = city_template | openai_llm | json_parser | {
    "restaurants": restaurants_template | openai_llm,
    "activities": cultural_activities_template | openai_llm,
    "city": itemgetter("city"),
    "interest": itemgetter("interest"),
} | response_template | openai_llm
response = chain.invoke({"interest": "swimming"})
print("======")
print(response.content)

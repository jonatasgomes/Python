import pandas as pd
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.experimental.query_engine import PandasQueryEngine
import textwrap
import os
import env
import logging

def output_response(response):
    print(textwrap.fill(response.response, width=100))

url = os.path.join(os.path.dirname(__file__), 'vendas.csv')
data = pd.read_csv(url)

logging.getLogger("httpx").setLevel(logging.WARNING)
Settings.llm = Groq(model='llama3-70b-8192', api_key=env.GROQ_API_KEY)
query_engine = PandasQueryEngine(df=data) # , verbose=False, synthesize_response=True)
response = query_engine.query('Qual é a média de gasto por tipo de cliente?')
output_response(response)

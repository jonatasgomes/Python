import gradio as gr
import pandas as pd
from llama_index.core import PromptTemplate
from llama_index.llms.groq import Groq
from llama_index.experimental.query_engine import PandasInstructionParser
from llama_index.core.query_pipeline import (QueryPipeline as QP, Link, InputComponent)
import env

def load_data(file_path, df_state):
  if file_path is None or file_path == "":
    return 'No file uploaded', df_state
  try:
    df = pd.read_csv(file_path)
    return 'File uploaded successfully', df
  except Exception as e:
    return f'Error loading file: {e}', df_state

def cols_description(df):
  desc = '\n'.join([f"`{col}`: {str(df[col].dtype)}" for col in df.columns])
  return 'Here are the columns in the dataframe:\n' + desc

def pipeline_query(df):
  instruction_str = (
      "1. Convert the query to executable Python code using Pandas.\n"
      "2. The final line of code should be a Python expression that can be called with the `eval()` function.\n"
      "3. The code should represent a solution to the query.\n"
      "4. PRINT ONLY THE EXPRESSION.\n"
      "5. Do not quote the expression.\n"
  )

  pandas_prompt_str = (
      "You are working with a pandas dataframe in Python.\n"
      "The name of the dataframe is `df`.\n"
      "{cols_description}\n\n"
      "This is the result of `print(df.head())`:\n"
      "{df_str}\n\n"
      "Follow these instructions:\n"
      "{instruction_str}\n"
      "Query: {query_str}\n\n"
      "Expression:"
  )
  response_synthesis_prompt_str = (
      "Given an input question, act as a data analyst and synthesize a response from the query results.\n"
      "Answer in a natural language response using Brazilian Portuguese and do not use introductions like 'A resposta é:' or similar.\n"
      "Query: {query_str}\n\n"
      "Pandas Instructions (optional):\n{pandas_instructions}\n\n"
      "Pandas Output: {pandas_output}\n\n"
      "Response: "
  )

  pandas_prompt = PromptTemplate(pandas_prompt_str).partial_format(
      instruction_str=instruction_str,
      cols_description=cols_description(df),
      df_str=str(df.head()),
  )
  pandas_output_parser = PandasInstructionParser(df)
  response_synthesis_prompt = PromptTemplate(response_synthesis_prompt_str)
  llm = Groq(model='llama3-70b-8192', api_key=env.GROQ_API_KEY)
  qp = QP(
      modules={
          "input": InputComponent(),
          "pandas_prompt": pandas_prompt,
          "llm1": llm,
          "pandas_output_parser": pandas_output_parser,
          "response_synthesis_prompt": response_synthesis_prompt,
          "llm2": llm
      },
      verbose=False
  )
  qp.add_chain(["input", "pandas_prompt", "llm1", "pandas_output_parser"])
  qp.add_links(
      [
          Link("input", "response_synthesis_prompt", dest_key="query_str"),
          Link("llm1", "response_synthesis_prompt", dest_key="pandas_instructions"),
          Link("pandas_output_parser", "response_synthesis_prompt", dest_key="pandas_output")
      ]
  )
  qp.add_link("response_synthesis_prompt", "llm2")
  return qp

def process_query(query, df_state):
  if df_state is not None and query:
    qp = pipeline_query(df_state)
    response = qp.run(query_str=query)
    return response.message.content
  return ''

with gr.Blocks() as app:
  input_file = gr.File(label="Upload CSV file", file_count='single', type='filepath')
  upload_status = gr.Textbox(label="Upload Status")
  input_query = gr.Textbox(label="Query", lines=5, placeholder="Enter a query")
  submit_button = gr.Button("Submit")
  output_response = gr.Textbox(label="Response", lines=5, placeholder="Response will appear here")
  pdf_file = gr.File(label="Download PDF")
  
  df_state = gr.State(value=None)
  input_file.change(fn=load_data, inputs=[input_file, df_state], outputs=[upload_status, df_state])
  submit_button.click(fn=process_query, inputs=[input_query, df_state], outputs=[output_response])


app.launch(debug=True)

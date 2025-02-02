from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import os
import env

# 1. load the data
path = os.path.dirname(__file__)
loader = CSVLoader(file_path=path + "/data/rag.csv")
documents = loader.load()

# 2. load the embeddings
embeddings = OpenAIEmbeddings(openai_api_key=env.OPENAI_KEY)
vector_store = FAISS.from_documents(documents, embeddings)
retriever = vector_store.as_retriever()

# 3. create the llm
llm = ChatOpenAI(api_key=env.OPENAI_KEY)
prompt = ChatPromptTemplate.from_template(
  """
    Your work is to give a simple and precise answer to the given question below based on the following context:
    Context: {context}
    Question: {question}
  """
)

# 4. create the chain/pipeline
chain = (
  { "context": retriever, "question": RunnablePassthrough() }
  | prompt
  | llm
)

# 5. run the chain
while True:
  question = input("You: ")
  response = chain.invoke(question)
  print("Bot:", response.content)

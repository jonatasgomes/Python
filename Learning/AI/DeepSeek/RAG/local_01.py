import os

os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                           "AppleWebKit/537.36 (KHTML, like Gecko) " \
                           "Chrome/91.0.4472.124 Safari/537.36"

from langchain_community.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
import re

# Step 1: Load documents (e.g., from a website or database)
loader = WebBaseLoader("https://en.wikipedia.org/wiki/Politics_of_Brazil")

# Step 2: Set up an embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 3: Create a vector store index with the embedding model
index = VectorstoreIndexCreator(
    vectorstore_cls=FAISS,
    embedding=embedding_model
).from_loaders([loader])

# Step 4: Set up the retrieval-augmented generation chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OllamaLLM(model="llama3:latest", temperature=0.0),
    chain_type="stuff",
    retriever=index.vectorstore.as_retriever(),
    return_source_documents=False
)

# Step 5: Ask a question
while True:
    query = input("You: ")
    response = qa_chain.invoke({"query": query}, return_only_outputs=True)
    response = response['result']
    response = re.sub(r'<think>.*?</think>\n\n', '', response, flags=re.DOTALL)
    print("Bot:", response)

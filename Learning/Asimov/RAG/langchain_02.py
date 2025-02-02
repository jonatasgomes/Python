import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_ollama import ChatOllama, OllamaEmbeddings
import os

model_local = ChatOllama(model="llama3:latest")

@st.cache_resource
def load_csv_data():
    loader = CSVLoader(file_path=os.path.join(os.path.dirname(__file__), "data/rag.csv"))
    documents = loader.load()
    embeddings = OllamaEmbeddings(model='nomic-embed-text')
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    return retriever

retriever = load_csv_data()
st.title("Local Chat")

rag_template = """
You are a chatbot.
Your job is to converse with users by consulting the knowledge base 
and to provide them with a simple and precise answer based on 
the database provided as context. Always answer in the same language 
as the question. Do not mention the context or the database.
Just provide the simple and direct answer.

Context: {context}

Customer's question: {question}
"""
prompt = ChatPromptTemplate.from_template(rag_template)
chain = prompt | model_local  # Simplified chain since you'll provide formatted strings

# Initialize session state for messages if needed
if "messages" not in st.session_state:
    st.session_state.messages = []

# Capture new user input
user_input = st.chat_input("You: ")
if user_input:
    # Append the user's message to the conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Retrieve context (example using the new recommended `invoke` method)
    docs = retriever.invoke(user_input)
    # Combine document content into a single string; adjust as needed.
    context_str = "\n".join(doc.page_content for doc in docs)
    
    # Prepare the prompt input with plain strings
    prompt_input = {"context": context_str, "question": user_input}
    
    # Process the chain to get the assistant's response
    response_stream = chain.stream(prompt_input)
    full_response = ""
    for partial_response in response_stream:
        full_response += str(partial_response.content)
    
    # Append the assistant's response to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Render the entire conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

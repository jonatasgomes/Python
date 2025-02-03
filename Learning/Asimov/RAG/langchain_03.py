import streamlit as st
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
import data.oracle_connection as db

model_local = ChatOllama(model="llama3:latest", temperature=0.0)

def generate_sql_query(user_question, schema_info):
    prompt = f"""
    I have an Oracle database with the following schema:
    Tables:
    1. st1_stocks: columns (id number, ticker varchar2(30))
    2. st1_stock_prices: columns (stock_id number, price_dt date, close number, timeframe varchar2(30))
       timeframe column should be '1d'.

    Here is an example query to get the price of AAPL stock from 2025-01-01:
     select s.ticker, sp.price_dt, sp.close
       from st1_stock_prices sp, st1_stocks s
      where s.ticker = 'AAPL'
        and sp.stock_id = s.id
        and sp.price_dt >= to_date('2025-01-01', 'yyyy-mm-dd')
        and sp.timeframe = '1d'
      order by s.ticker, sp.price_dt
    
    The user asks the following question: "{user_question}"

    Please generate the SQL query to answer this question using the provided schema.
    Always return 3 columns: ticker, price_dt, close.
    Return just the SQL query text without any special character and no introduction text.
    The returned SQL must starts with 'select' and ends with 'order by s.ticker, sp.price_dt'.
    """
    response = model_local.invoke(prompt)
    sql_query = response.content
    return sql_query

@st.cache_resource
def load_rag_data(question):
    schema_info = {
        "tables": [
            {"name": "st1_stocks", "columns": ["id", "ticker"]},
            {"name": "st1_stock_prices", "columns": ["stock_id", "price_dt", "close", "timeframe"]}
        ]
    }
    sql_query = generate_sql_query(question, schema_info)
    raw_data = db.execute_sql_query(sql_query)
    if isinstance(raw_data, str):
        return None
    else:
        documents = []
        for row in raw_data:
            content = f"Ticker: {row[0]}, Date: {row[1]}, Price: {row[2]}"
            document = Document(page_content=content)
            documents.append(document)
        embeddings = OllamaEmbeddings(model='nomic-embed-text')
        vectorstore = FAISS.from_documents(documents, embeddings)
        retriever = vectorstore.as_retriever()
        return retriever

st.title("Local Chat")

rag_template = """
Your job is to provide the price of a ticker on a specific date.
The below provided context has the json format of the ticker, date, and price.

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
    st.session_state.messages.append({"role": "user", "content": user_input})
    retriever = load_rag_data(user_input)
    if retriever is None:
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't generate the SQL query."})
    else:
        docs = retriever.invoke(user_input)
        context_str = "\n".join(doc.page_content for doc in docs)
        prompt_input = {"context": context_str, "question": user_input}
        response_stream = chain.stream(prompt_input)
        full_response = ""
        for partial_response in response_stream:
            full_response += str(partial_response.content)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Render the entire conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

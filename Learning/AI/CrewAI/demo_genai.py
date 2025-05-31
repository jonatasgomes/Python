from langchain_google_genai import ChatGoogleGenerativeAI
import env

# Initialize the chat model
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=env.GENAI_API_KEY)

# Create a conversation
messages = [
    {"role": "user", "content": "What is machine learning?"}
]

# Get response
response = chat.invoke(messages)

# Print the response
print(response.content)

# Continue conversation
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": "Can you give me an example?"})

# Get another response
response = chat.invoke(messages)
print(response.content)
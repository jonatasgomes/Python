from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_ollama import OllamaLLM
# from langchain.globals import set_debug

# set_debug(True)
memory = ConversationBufferWindowMemory(k=2)
llm = OllamaLLM(
    model="llama3",
    temperature=0.7,
    base_url="http://localhost:11434"
)
conversation = ConversationChain(
    llm=llm,
    memory=memory
)

messages = [
    "Tell me about a nice city for swimming on warm waters.",
    "What are the main places to visit there?",
    "What are 20 other cities with the same conditions ordered from the best including the one mentioned?",
    "For the first city from the beginning, tell me the 3 best places to swim.",
]
for message in messages:
    try:
        response = conversation.predict(input=message)
        print(response)
        print("===" * 20)
        print(memory.load_memory_variables({}))
    except Exception as e:
        print(e.__doc__)
        exit(1)

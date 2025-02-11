import nltk
from nltk.chat.util import Chat

# Dicionário personalizado de reflections
reflections_personalizados_somente_nas_respostas_do_chat = {
    "eu": "você",
    "meu": "seu",
    "minha": "sua",
    "meus": "seus",
    "minhas": "suas",
    "seu": "meu",
    "sua": "minha",
    "seus": "meus",
    "suas": "minhas",
    "vou": "vai",
    "era": "fui"
}

# Pares de padrões e respostas
pares = [
    [
        r"meu nome é (.*)",  # Captura o nome do usuário
        ["Olá, %1! Como posso ajudar hoje ?"]
    ],
    [
        r"eu sou (.*)",  # Captura informações sobre quem o usuário é
        ["Por que você é %1? Me conte mais."]
    ],
    [
        r"meu (.*) é (.*)", # Captura algo que o usuário possui
        ["Por que meu %1 é %2? Isso parece interessante."]
    ],
    [
        r"como você está?", # Pergunta sobre o estado do chatbot
        ["Estou bem, obrigado por perguntar! E eu ?"]
    ],
    [
        r"(.*) você gosta de (.*)",  # Pergunta sobre os gostos do chatbot
        ["Não sei se gosto de %2, mas e você ?"]
    ],
    [
        r"sair",  # Comando para encerrar a conversa
        ["Tchau! Foi um prazer conversar com você. Até a próxima!"]
    ],
    [
        r"(.*)",  # Resposta genérica para entradas não reconhecidas
        ["Desculpe, não entendi. Pode reformular a pergunta?"]
    ]
]

# Função para aplicar reflections apenas nas respostas
def aplicar_reflections(texto, reflections):
    palavras = texto.lower().split()
    resposta_transformada = [reflections.get(palavra, palavra) for palavra in palavras]
    return " ".join(resposta_transformada)

# Criando o chatbot
chatbot = Chat(pares, reflections_personalizados_somente_nas_respostas_do_chat)

# Testando o chatbot
print("Chatbot: Olá! Sou um chatbot. Diga 'sair' para encerrar a conversa.")
while True:
    entrada = input("Você: ")
    if entrada.lower() == "sair":
        print("Chatbot: Tchau! Foi um prazer conversar com você.")
        break

    # Obtém a resposta sem modificar a entrada
    resposta = chatbot.respond(entrada)
    
    # Aplica reflections na resposta, não na entrada
    if resposta:
        resposta_transformada = aplicar_reflections(resposta, reflections_personalizados_somente_nas_respostas_do_chat)
        print(f"Chatbot: {resposta_transformada}")
    else:
        print("Chatbot: Desculpe, não entendi sua pergunta.")

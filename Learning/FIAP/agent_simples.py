class Ambiente:
    def __init__(self):
        # Define o ambiente como uma matriz 2x2 (4 cômodos)
        self.casas = [
            ["sujo", "sujo"],
            ["sujo", "sujo"]
        ]

    def exibir_ambiente(self):
        print("Estado atual do ambiente:")
        for linha in self.casas:
            print(linha)

class Agente:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.posicao = [0, 0]  # Começa no canto superior esquerdo (0,0)

    def perceber(self):
        # Observa o estado da casa atual
        x, y = self.posicao
        return self.ambiente.casas[x][y]

    def decidir_acao(self, estado):
        # Decide a ação com base no estado percebido
        if estado == "sujo":
            return "limpar"
        return "mover"

    def agir(self, acao):
        # Executa a ação decidida
        if acao == "limpar":
            x, y = self.posicao
            self.ambiente.casas[x][y] = "limpo"
            print(f"Limpando a posição {self.posicao}")
        elif acao == "mover":
            self.mover()

    def mover(self):
        # Move o agente para a próxima posição (simplesmente para a direita ou para baixo)
        x, y = self.posicao
        if y < len(self.ambiente.casas[0]) - 1:  # Move para a direita, se possível
            self.posicao = [x, y + 1]
        elif x < len(self.ambiente.casas) - 1:  # Move para baixo, se possível
            self.posicao = [x + 1, 0]
        else:
            print("Fim do ambiente. Nada mais a fazer.")
            self.posicao = None  # Agente para ao final do ambiente
        print(f"Movendo para {self.posicao}")

    def executar(self):
        # Loop principal do agente
        while self.posicao is not None:
            estado = self.perceber()
            acao = self.decidir_acao(estado)
            self.agir(acao)
            self.ambiente.exibir_ambiente()

# Criando o ambiente e o agente
ambiente = Ambiente()
agente = Agente(ambiente)

# Exibindo o estado inicial do ambiente
ambiente.exibir_ambiente()

# Executando o agente
agente.executar()

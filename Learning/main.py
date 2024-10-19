with open("exemplo.txt", "w") as arquivo:
    arquivo.write("Olá, Mundo!\n")
    arquivo.write("Python é incrível!\n")

with open("exemplo.txt", "r") as arquivo:
    conteudo = arquivo.read()
    print(conteudo)

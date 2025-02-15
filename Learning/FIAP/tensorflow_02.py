import tensorflow as tf
import os

# Carregar o modelo treinado
path = os.path.join(os.path.dirname(__file__), "saude_model.keras")
model = tf.keras.models.load_model(path)

# Função para normalizar os dados (baseado no pré-processamento usado durante o treinamento)
def normalizar_dados(temperatura, freq_cardiaca):
    temp_norm = temperatura / 40.0  # Normaliza temperatura para escala 0-1
    freq_norm = freq_cardiaca / 120.0  # Normaliza frequência cardíaca para escala 0-1
    return [temp_norm, freq_norm]

# Função para classificar a entrada
def classificar_saude(temperatura, freq_cardiaca):
    # Normalizar os dados
    entrada_normalizada = normalizar_dados(temperatura, freq_cardiaca)
    entrada_tensor = tf.convert_to_tensor([entrada_normalizada], dtype=tf.float32)

    # Fazer a predição
    probabilidade = model.predict(entrada_tensor)[0][0]
    rotulo = "Saúde" if probabilidade >= 0.5 else "Risco"
    
    return rotulo, probabilidade

# Loop para receber dados do ESP32 via input manual
print("Insira os dados de temperatura e frequência cardíaca do ESP32:")
while True:
    try:
        # Recebe dados do usuário
        temperatura = float(input("Temperatura (°C): "))
        freq_cardiaca = float(input("Frequência Cardíaca (BPM): "))

        # Classificar os dados
        rotulo, probabilidade = classificar_saude(temperatura, freq_cardiaca)

        # Exibir o resultado
        print(f"\nResultado da Classificação:")
        print(f"Temperatura: {temperatura} °C")
        print(f"Frequência Cardíaca: {freq_cardiaca} BPM")
        print(f"Classificação: {rotulo} ({probabilidade*100:.2f}%)")

    except ValueError:
        print("Por favor, insira valores numéricos válidos para temperatura e frequência cardíaca.")
    except KeyboardInterrupt:
        print("\nSaindo do programa.")
        break

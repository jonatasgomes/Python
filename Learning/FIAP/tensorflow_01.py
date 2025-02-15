import tensorflow as tf
import numpy as np
import os #para facilitar a encontrar o arquivo resultante (modelo)

# Dados de entrada (temperatura e frequência cardíaca) e saída (saúde)
# 1ª coluna: temperatura (°C), 2ª coluna: frequência cardíaca (BPM)
X = np.array([
    [36.5, 70],
    [39.0, 100],
    [35.5, 60],
    [40.0, 120],
    [37.0, 80],
    [38.5, 95],
    [36.8, 75]
])

# Saídas correspondentes (saudável ou risco)
y = np.array([1, 0, 1, 0, 1, 0, 1])  # 1 = saudável, 0 = risco

# Normalização dos dados
X = X / np.array([40.0, 120.0])  # Escala máxima para normalização

# Construção do modelo
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(2,)),  # Camada oculta com 16 neurônios
    tf.keras.layers.Dense(8, activation='relu'),                    # Camada oculta com 8 neurônios
    tf.keras.layers.Dense(1, activation='sigmoid')                  # Saída (probabilidade de saúde)
])

# Compilação do modelo
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Treinamento do modelo
model.fit(X, y, epochs=100, batch_size=4)

# Avaliação do modelo
loss, accuracy = model.evaluate(X, y)
print(f"Loss: {loss}, Accuracy: {accuracy}")

# Salvar o modelo
path = os.path.join(os.path.dirname(__file__), "saude_model.keras")
model.save(path)
print(os.listdir(os.path.dirname(__file__))) # Lista todos os arquivos no diretório atual, incluindo saude_model.keras

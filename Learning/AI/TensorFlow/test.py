import tensorflow as tf
from tensorflow import keras

print('Keras version:', keras.__version__)
print("TensorFlow version:", tf.__version__)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

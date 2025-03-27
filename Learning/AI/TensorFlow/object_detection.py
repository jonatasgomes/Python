import tensorflow as tf
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix
from keras import Sequential, layers, models
from keras.callbacks import EarlyStopping # type: ignore
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
from keras.utils import to_categorical # type: ignore
from tensorflow.keras.layers import Rescaling  # type: ignore
from tensorflow.keras.applications.vgg16 import VGG16 # type: ignore
from tensorflow.keras.applications.vgg16 import preprocess_input # type: ignore

(train_ds, train_labels), (test_ds, test_labels) = tfds.load(
  'tf_flowers',
  split=['train[:70%]', 'train[30%:]'],
  batch_size=-1,
  as_supervised=True
)
print(train_ds.shape, test_ds.shape, train_labels)

size = (150, 150)
train_ds = tf.image.resize(train_ds, size)
test_ds = tf.image.resize(test_ds, size)

train_labels = to_categorical(train_labels, num_classes=5)
test_labels = to_categorical(test_labels, num_classes=5)
print(train_ds.shape, test_ds.shape, train_labels)

hand_model = Sequential()
hand_model.add(Rescaling(1./255, input_shape=(150, 150, 3)))
hand_model.add(layers.Conv2D(16, kernel_size=10, activation='relu'))
hand_model.add(layers.MaxPooling2D(3))
hand_model.add(layers.Conv2D(32, kernel_size=8, activation='relu'))
hand_model.add(layers.MaxPooling2D(2))
hand_model.add(layers.Conv2D(32, kernel_size=6, activation='relu'))
hand_model.add(layers.MaxPooling2D(2))

hand_model.add(layers.Flatten())
hand_model.add(layers.Dense(50, activation='relu'))
hand_model.add(layers.Dense(20, activation='relu'))
hand_model.add(layers.Dense(5, activation='softmax'))

hand_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
es = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)

with tf.device('/device:GPU:0'):
  hand_model.fit(train_ds, train_labels, epochs=20, validation_split=0.2, batch_size=32, callbacks=[es])

loss, acc = hand_model.evaluate(test_ds, test_labels)
print(f'Accuracy: {acc:.27}, Loss: {loss:.2f}')
# epochs=5, Accuracy: 0.393149077892303466796875, Loss: 1.43
# epochs=10, Accuracy: 0.2977812290191650390625, Loss: 1.61
# epochs=4, Accuracy: 0.24678863584995269775390625, Loss: 3.98
# epochs=20, Accuracy: 0.434410274028778076171875, Loss: 1.33

def plot_confusion_matrix(y_test, y_pred):
  labels = list(map(np.argmax, y_test))
  labels_pred = list(map(np.argmax, y_pred))
  cm = confusion_matrix(labels, labels_pred)
  sns.heatmap(cm, annot=True, fmt='d')
  plt.show()

preds = hand_model.predict(test_ds)
plot_confusion_matrix(test_labels, preds)

train_dsTL = preprocess_input(train_ds)
test_dsTL = preprocess_input(test_ds)
base_model = VGG16(input_shape=train_dsTL[0].shape, include_top=False, weights='imagenet')
base_model.trainable = False
print(base_model.summary())

flatten_layer = layers.Flatten()
dense_layer_1 = layers.Dense(50, activation='relu')
dense_layer_2 = layers.Dense(20, activation='relu')
prediction_layer = layers.Dense(5, activation='softmax')

model = models.Sequential([
  base_model,
  flatten_layer,
  dense_layer_1,
  dense_layer_2,
  prediction_layer
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
es = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)

with tf.device('/device:GPU:0'):
  model.fit(train_dsTL, train_labels, epochs=20, validation_split=0.2, batch_size=32, callbacks=[es])

loss, acc = model.evaluate(test_dsTL, test_labels)
print(f'Accuracy: {acc:.2f}, Loss: {loss:.2f}')

preds = model.predict(test_dsTL)
plot_confusion_matrix(test_labels, preds)

# epochs=20, Accuracy: 0.769949376583099365234375, Loss: 4.27

print('Layers: ', len(base_model.layers))
base_model.trainable = True
fine_tune_at = 13
for layer in base_model.layers[:fine_tune_at]:
  layer.trainable = False

model_fn = models.Sequential([
  base_model,
  flatten_layer,
  dense_layer_1,
  dense_layer_2,
  prediction_layer
])

model_fn.summary()
model_fn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
es = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)
with tf.device('/device:GPU:0'):
  history = model_fn.fit(train_dsTL, train_labels, epochs=40, validation_split=0.2, batch_size=32, callbacks=[es])

loss, acc = model_fn.evaluate(test_dsTL, test_labels)
print(f'Accuracy: {acc:.2f}, Loss: {loss:.2f}')

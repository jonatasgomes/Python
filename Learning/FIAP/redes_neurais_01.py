import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

iris = load_iris()
data = pd.DataFrame(iris.data, columns=iris.feature_names)
data['class'] = iris.target
print(data)

x = data.drop('class', axis=1)
y = data['class']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# p = Perceptron(random_state=42)
# p.fit(x_train, y_train)
# y_pred = p.predict(x_test)

def confusion_matrix_f(test_labels, test_preds, labels):
    cm = confusion_matrix(test_labels, test_preds, labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap='Blues')
    plt.show()

# confusion_matrix_f(y_test, y_pred, p.classes_)

# sns.pairplot(data, hue='class', vars=('sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'))
# plt.show()

# mlp = MLPClassifier(hidden_layer_sizes=(5, ), max_iter=200, random_state=42, verbose=True)
# mlp.fit(x_train, y_train)
# y_pred = mlp.predict(x_test)
# confusion_matrix_f(y_test, y_pred, mlp.classes_)
# print('Acc Test: ', accuracy_score(y_test, y_pred))

# mlp = MLPClassifier(hidden_layer_sizes=(5, ), max_iter=50, random_state=42, verbose=False, activation='logistic')
# mlp.fit(x_train, y_train)
# y_pred = mlp.predict(x_test)
# confusion_matrix_f(y_test, y_pred, mlp.classes_)
# print('Acc Test: ', accuracy_score(y_test, y_pred))

# mlp = MLPClassifier(hidden_layer_sizes=(5, ), max_iter=50, random_state=42, verbose=False, activation='logistic', solver='lbfgs')
# mlp.fit(x_train, y_train)
# y_pred = mlp.predict(x_test)
# confusion_matrix_f(y_test, y_pred, mlp.classes_)
# print('Acc Test: ', accuracy_score(y_test, y_pred))

# mlp = MLPClassifier(hidden_layer_sizes=(5, 3), max_iter=1000, random_state=42, verbose=False, activation='logistic', solver='adam', learning_rate='adaptive')
# mlp.fit(x_train, y_train)
# y_pred = mlp.predict(x_test)
# print('Acc Test: ', accuracy_score(y_test, y_pred))
# confusion_matrix_f(y_test, y_pred, mlp.classes_)

mlp = MLPClassifier(hidden_layer_sizes=(5, 3), solver='lbfgs')
mlp.fit(x_train, y_train)
y_pred = mlp.predict(x_test)
print('Acc Test: ', accuracy_score(y_test, y_pred))
confusion_matrix_f(y_test, y_pred, mlp.classes_)

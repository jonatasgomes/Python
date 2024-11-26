import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
import pandas as pd
import numpy as np

x, y = make_classification(
    n_samples=300,
    n_features=3,
    n_informative=3,
    n_redundant=0,
    n_clusters_per_class=1,
    n_classes=3,
    random_state=0
)

df = pd.DataFrame(x, columns=['Feature 1', 'Feature 2', 'Feature 3'])
df['Target'] = y
print(df.head())

plt.figure(figsize=(15, 5))
plt.scatter(df['Feature 1'], df['Feature 2'], c=df['Target'], cmap='viridis', edgecolors='k', s=50)
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Scatter Plot')
plt.colorbar(label='Target')
plt.grid(True)
plt.show()

fig = plt.figure(figsize=(15, 5))
ax = fig.add_subplot(111, projection='3d')
colors = plt.cm.viridis(df['Target'] / np.max(df['Target']))
scatter = ax.scatter(df['Feature 1'], df['Feature 2'], df['Feature 3'], c=colors, edgecolors='k', alpha=0.7)
ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')
ax.set_zlabel('Feature 3')
ax.set_title('3D Scatter Plot')
plt.show()

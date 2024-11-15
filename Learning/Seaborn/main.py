import pandas
import seaborn as sns
import matplotlib.pyplot as plt

df = pandas.DataFrame({'est_time': [1, 2, 3, 4, 5], 'est_cost': [20, 60, 75, 100, 140]})
sns.scatterplot(x='est_time', y='est_cost', data=df)
plt.show()
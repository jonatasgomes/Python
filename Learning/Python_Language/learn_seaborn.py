import matplotlib.pyplot as plt
import seaborn as sns

data = sns.load_dataset('tips')

plt.figure(figsize=(15, 5))
sns.swarmplot(data=data, x='day', y='total_bill', hue='time')
plt.show()

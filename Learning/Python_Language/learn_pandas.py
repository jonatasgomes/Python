import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sales = {
    'Day': range(1, 31),
    'Sales': np.random.randint(300, 2500, 30)
}

sales = pd.DataFrame(sales)
print(sales.describe())
sales.plot(x='Day', y='Sales', kind='line', marker='o', color='green')
plt.show()

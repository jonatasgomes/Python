import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(ncols=2, nrows=2)
ax1, ax2, ax3, ax4 = axs.flat

x, y = np.random.normal(size=(2, 200))
ax1.plot(x, y, 'o')

L = 2 * np.pi
x = np.linspace(0, L)
shift = np.linspace(0, L, 10, endpoint=False)
for s in shift:
    ax2.plot(x, np.sin(x + s), '-')

y1 = np.random.randint(1, 25, size=(1, 5))[0]
ax3.bar(np.arange(5), y1, 0.25, color='yellowgreen')

for c in ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']:
    x, y = np.random.normal(size=2)
    ax4.add_patch(plt.Circle((x, y), radius=0.3, color=c))
ax4.axis('equal')

plt.show()

import numpy
import matplotlib.pyplot as plt

prob_a = 0.5
prop = []
a = 0
c = 1
for i in range(1000):
    if numpy.random.rand() < prob_a:
        a += 1
    prop += [a / c]
    c += 1

# print(prop)
plt.plot(prop)
plt.show()

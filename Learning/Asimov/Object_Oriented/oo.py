import random

num = []
for i in range(6):
    num.append(random.choice([i for i in range(1, 60) if i not in num]))
num.sort()
print(num)

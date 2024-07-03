import pdb

x = 10
pdb.set_trace()
x = x ** 2
print(x)

try:
    print(x/0)
except Exception as e:
    print(e)
else:
    print('x is ok')
finally:
    print('done')
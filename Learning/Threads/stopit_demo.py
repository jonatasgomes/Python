from stopit import threading_timeoutable as timeoutable

@timeoutable()
def count():
    i = 0
    for i in range(10**9):
        i = i * 2
    return i

result = count(timeout=5)
print(result)

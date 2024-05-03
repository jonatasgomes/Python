def d(x):
    def w(*arg):
        print(f'{x.__name__} started. {arg}')
        return x(*arg)
    return w

@d
def greet(name):
    print(name)

greet('John')

def f_params(*args, **nargs):
    [print(arg) for arg in args]
    [print(key, '=', value) for key, value in nargs.items()]

f_params(1, 2, 3, name='John', age=20)

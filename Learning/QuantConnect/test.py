class Test:
    value = 189
    def __init__(self):
        value = 'abc'
    def get_value(self):
        return self.value

test = Test()
test.value = 190
Test.value = 191
print(test.get_value(), Test.value)

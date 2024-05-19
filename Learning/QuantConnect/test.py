import datetime


class Test:
    my_time = datetime.time.min

    def __init__(self):
        self.my_time = datetime.datetime.now()


test = Test()
print(Test.my_time, test.my_time)

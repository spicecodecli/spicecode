# Python sample for function counting
def func1():
    pass

class MyClass:
    def method1(self):
        pass

    def _private_method(self):
        # def nested_func(): pass # This shouldn't be counted by simple regex
        pass

def func2(a, b):
    return a + b

# def commented_out(): pass

lambda_func = lambda x: x * 2

def func_with_decorator():
    pass


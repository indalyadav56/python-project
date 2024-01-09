from queue import Queue

class MyClass:
    def __init__(self):
        print("Initializing MyClass")

    @staticmethod
    def my_static_method():
        print("Inside static method")

# Creating an instance of MyClass
# obj = MyClass()

# Calling the static method
MyClass.my_static_method()

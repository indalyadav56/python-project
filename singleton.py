# 1. Simple Approach:

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

# 2. Metaclass Approach:
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    pass

# 3. Module Approach:
# In a module named singleton.py
_instance = None

def get_instance():
    global _instance
    if not _instance:
        _instance = Singleton()
    return _instance

class Singleton:
    def __init__(self):
        pass  # Do initialization here

# 4. functools.cached_property Approach (Python 3.8+):

from functools import cached_property

class Singleton:
    @cached_property
    def instance(self):
        return self

instance = Singleton().instance





import ctypes


class Array:
    def __init__(self) -> None:
        self.size = 1
        self.n = 1
        self.__make_array__(self.size)

    def __make_array__(self, size):
        return (size*ctypes.py_object)()

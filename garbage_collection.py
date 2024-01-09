# import gc
# import sys

# all_objects = gc.get_objects()

# for obj in all_objects:
#     if isinstance(obj, list):
#         print(id(obj), sys.getsizeof(obj))


import sys

my_list = [1, 2, 3, "hello"]
print(sys.getsizeof(my_list))  # Output: 88 (bytes)

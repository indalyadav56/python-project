def feb(n):
    if (n == 1):
        return 0
    elif (n == 2):
        return 1
    return feb(n - 1) + feb(n - 2)


print(feb(5))

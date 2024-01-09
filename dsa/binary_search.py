l = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
s = 0
e = 9
key = 100
present = 0
for i in l:
    m = int((s+e)/2)
    if key == l[m]:
        present = key
    if key > l[m]:
        s = m+1
    else:
        e = m-1
print(present)

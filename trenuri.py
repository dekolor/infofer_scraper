trenuri = []
f = open("trenuri.txt", "r")
for x in f:
    tren = x.split(",")[2]
    trenuri.append(tren)
f.close()
print(trenuri)
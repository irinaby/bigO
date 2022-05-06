n = 0
for d in range(x, 0, -1):
    for c in range(d, 0, -1):
        for b in range(c, 0, -1):
            a = x - d - c - b;
            if (a > 0 and a <= b):
                n += 1
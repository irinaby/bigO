from itertools import chain, combinations

z=[]
for r in range(0, len(lst)):
    for c in combinations(lst, r + 1):
        z.append(list(c))

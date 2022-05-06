import clipboard
from numpy import log2, power, prod, array, seterr
from scipy.optimize import curve_fit

def constFn(x, a):
    return [a] * len(x)

def linearFn(x, a, b):
    return a * x + b

def quadraticFn(x, a, b, c):
    return a * x**2 + b * x + c

def cubicFn(x, a, b, c, d):
    return a * x**3 + b * x ** 2 + c * x + d

def logarithmicFn(x, a, b, c):
    if (b <= 0): return [0] * len(x)
    return a * log2(b * x) + c

def linearithmicFn(x, a, b, c):
    if (b <= 0): return  [0] * len(x)
    return a * x * log2(b * x) + c

def exponentialFn(x, a, b, c):
    return a * power(2, b * x) + c

def factorialFn(x, a, b):
    return list(a * prod(range(1, int(k) + 1)) + b for k in x)

bubble_x = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
bubble_y = [0, 5, 27, 119, 495, 2015, 8127, 32639, 130815, 523775, 2096127]

binsearch_x = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
binsearch_y = [0, 2, 1, 0, 3, 4, 6, 5, 6, 8, 10, 10, 9, 13, 14, 14, 16, 16, 14, 19]

salesman_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
salesman_y = [1, 3, 8, 27, 124, 725, 5046, 40327, 362888, 3628809]

cubic_x = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
cubic_y = [1539, 11479, 37819, 88559, 171699, 295239, 467179, 695519, 988259, 1353399]

powerset_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
powerset_y = [0, 2, 6, 14, 30, 62, 126, 254, 510, 1022, 2046, 4094, 8190, 16382, 32766, 65534, 131070, 262142, 524286, 1048574]

merge_x = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
merge_y = [4, 15, 40, 92, 223, 516, 1152, 2555, 5644, 12316, 26659]

metrics = [
    ("binsearch", binsearch_x, binsearch_y),
    ("merge", merge_x, merge_y),
    ("bubble", bubble_x, bubble_y),
    ("cubic", cubic_x, cubic_y),
    ("powerset", powerset_x, powerset_y),
    ("salesman", salesman_x, salesman_y)
]

fns = [constFn, linearFn, logarithmicFn, linearithmicFn, quadraticFn, cubicFn, exponentialFn, factorialFn]
#seterr(all='raise')
r=""
for algo, x, y in metrics:
    print(algo)
    bestYY = []
    bestRMSE = -1
    bestFn = ""
    sbestYY = []
    sbestRMSE = -1
    sbestFn = ""

    for fn in fns:
        if (x[-1] > 32 and fn == exponentialFn):
            print("%s: RMSE = %s" % (fn.__name__, 'not tested'))
            continue

        #try:
        popt, _ = curve_fit(fn, x, y, method='trf')
        #except (OptimizeWarning, FloatingPointError):
        #    print("%s: RMSE = %s" % (fn.__name__, 'not tested'))
        #    continue

        yy = fn(array(x), *popt)

        rmse = 0
        for y1, y2 in zip(y, yy):
            rmse += (y1 - y2) ** 2
        rmse = rmse / len(y) ** 0.5

        print("%s: RMSE = %s" % (fn.__name__, rmse))

        if (bestRMSE == -1 or rmse < bestRMSE):
            sbestFn = bestFn
            sbestRMSE = bestRMSE
            sbestYY = bestYY
            bestRMSE = rmse
            bestYY = yy
            bestFn = fn.__name__
    
    r += algo + "\t" + bestFn + "\t" + sbestFn + "\n"
    for z in zip(x, y, bestYY, sbestYY):
        r += ("%s\t%s\t%s\t%s\n" % z)
    r+="\n"
    print()

clipboard.copy(r)
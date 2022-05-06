import clipboard
import time
from pprint import pprint
import tracemalloc
import importlib
import sys
import io
import os

lastLine = -1
stepsCount = 0
afterJump = False

def trace_lines(frame, event, arg):
    global lastLine, stepsCount, afterJump
    if event != 'line' or frame.f_code.co_filename != "code_under_test":
        return
    #first_size, first_peak = tracemalloc.get_traced_memory()
    if (frame.f_lineno > lastLine):
        if (afterJump):
            stepsCount += 1
            afterJump = False
    else:
        afterJump = True
    lastLine = frame.f_lineno
    #print(frame.f_lineno, repsCount, file=sys.stderr)

def trace_calls(frame, event, arg):
    return trace_lines

def readAllText(path):
    with open(path, encoding='utf-8-sig') as f: return f.read()

def readAllLines(path):
    with open(path, encoding='utf-8-sig') as f: return f.read().splitlines();

def getTests(testsFile):
    return readAllLines(os.path.join(os.getcwd(), 'testdata', testsFile))

def getCode(algoFile):
    return readAllText(os.path.join(os.getcwd(), 'algo', algoFile))

def measure(codeFile, testsFile, prepareFn):
    global lastLine, stepsCount, afterJump
    code = getCode(codeFile)
    cmd = compile(code, "code_under_test", "exec")
    outX, outY = [], []
    for testLine in getTests(testsFile):
        lastLine = -1
        stepsCount = 0
        afterJump = False

        testFile, n = testLine.split(' ')
        testData = readAllText(os.path.join(os.getcwd(), 'testdata', testFile))
        sys.stdin = io.StringIO(testData)
        out_file = io.StringIO('')
        sys.stdout = out_file
        tracemalloc.start()
        testVars = prepareFn()
        sys.settrace(trace_calls)
        exec(cmd, testVars)
        sys.settrace(None)
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        print(out_file.getvalue())
        outX.append(n)
        outY.append(stepsCount)
    return outX, outY

def prepareBubble():
    n = int(input())
    lst = []
    for i in range(n):
        lst.append(int(input()))
    return {'n': n, 'lst': lst}

def prepareBinsearch():
    x = int(input())
    n = int(input())
    lst = []
    for i in range(n):
        lst.append(int(input()))
    return {'x': x, 'lst': lst}

def prepareSalesman():
    n = int(input())
    graph = []
    for j in range(n):
        r = []
        for i in input().split():
            r.append(int(i))
        graph.append(r)
    return {'s': 0, 'n': n, 'graph': graph}

def prepareCubic():
    x = int(input())
    return {'x': x}

def preparePowerset():
    n = int(input())
    lst = []
    for i in range(n):
        lst.append(input())
    return {'lst': lst}

r = ""
for codeFile, testsFile, prepareFn in [
    ('bubble.py', 'bubble.txt', prepareBubble),
    ('binsearch.py', 'binsearch.txt', prepareBinsearch),
    ('salesman.py', 'salesman.txt', prepareSalesman),
    ('cubic.py', 'cubic.txt', prepareCubic),
    ('powerset.py', 'powerset.txt', preparePowerset),
    ('merge.py', 'bubble.txt', prepareBubble)
]:
    x, y = measure(codeFile, testsFile, prepareFn)
    r += codeFile.partition('.')[0] + "_x = [" + ", ".join(map(str, x)) + "]\n"
    r += codeFile.partition('.')[0] + "_y = [" + ", ".join(map(str, y)) + "]\n"
    r+= "\n"

clipboard.copy(r)
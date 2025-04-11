import sys
import io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

marks = ".?!"

def input():
    s = sys.stdin
    return s

def output(s):
    print(s)
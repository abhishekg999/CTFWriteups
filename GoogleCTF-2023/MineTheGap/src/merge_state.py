import sys

with open('gameboard.txt', 'r') as main:
    mdata = [list(line) for line in main.read().split('\n')]
    with open(sys.argv[1], 'r') as f:
        fdata = [list(line) for line in f.read().split('\n')]

        for i, (l1, l2) in enumerate(zip(mdata, fdata)):
            for j, (val1, val2) in enumerate(zip(l1, l2)):
                if val2 == 'X':
                    mdata[i][j] = 'X'
            
from time import time
with open(f'modified{time()}.txt', 'w+') as f:
    for line in mdata:
        f.write(f"{''.join(line)}\n")
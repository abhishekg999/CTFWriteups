import sys

with open('gameboard.txt', 'r') as main:
    mdata = [list(line) for line in main.read().split('\n')]


import re

# Define the regular expression pattern
pattern = r"define-fun C(\d+)_(\d+) \(\) Int\n  (\d)"

# Open the file and parse its contents
with open("model.txt", "r") as file:
    contents = file.read()
    matches = re.findall(pattern, contents)

    # Set values in the 2D array based on the parsed matches
    for match in matches:
        row = int(match[0])
        col = int(match[1])
        value = int(match[2])

        if value == 0:
            mdata[row][col] = '9'
        elif value == 1:
            mdata[row][col] = 'B'
        else:
            assert False



from time import time
with open(f'FINAL_MERGE.txt', 'w+') as f:
    for line in mdata:
        f.write(f"{''.join(line)}\n")
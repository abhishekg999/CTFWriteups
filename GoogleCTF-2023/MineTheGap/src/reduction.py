import sys
from collections import deque

with open("gameboard.txt", "r") as fin:
    circuit = fin.read()
    circuit = circuit.replace(" ", "0")
    circuit = [list(line) for line in circuit.split("\n")]

print(len(circuit), len(circuit[0]))

# we will repeatedly solve by reducing the minesweeper board by subtracting the flag count.
# then force any existing solution

class Cell:
    __slots__ = ('value',)
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return self.value

class Flag(Cell):
    __slots__ = ('connections',)
    def __init__(self, value) -> None:
        super().__init__(value)
        self.connections = set()

    def add_connection(self, x, y):
        self.connections.add((x, y))


board = []

unhandled_flags_cnt = 0
unhandled_flags = set()


for x, line in enumerate(circuit):
    inner_row = []
    for y, cell in enumerate(line):
        if cell == "B" or cell == 'X':
            c = Flag(cell)
            unhandled_flags_cnt += 1
            unhandled_flags.add((x, y))

        else:
            c = Cell(cell)
        
        inner_row.append(c)
    board.append(inner_row)


saved_unhandled_flags = unhandled_flags.copy()

def getNeighbors(i, j):
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if x == i and y == j:
                continue
            yield x, y


DONT_TOUCH = set(["0", "B", "9", "X"])
window_origins = deque()

def reduce():
    global window_origins
    
    to_be_removed = []
    special_handling_set = set()

    #print(unhandled_flags)
    while unhandled_flags:
        i, j = unhandled_flags.pop()
        assert type(board[i][j]) == Flag
        # # decrement all neighbors that refer to it
        # dead_cnt = 0
        for nx, ny in getNeighbors(i, j):
            if board[nx][ny].value not in DONT_TOUCH and (nx, ny) not in board[i][j].connections:     
                affected_cell_value = int(board[nx][ny].value)
                if affected_cell_value == 1:
                    # needs to be specially handled later
                    special_handling_set.add((nx, ny))

                board[nx][ny].value = str(affected_cell_value - 1)
                board[i][j].add_connection(nx, ny)

                window_origins.append((nx, ny))

            # if board[nx][ny].value == '0' or board[nx][ny].value == 'B' or board[nx][ny].value == 'X':
            #     dead_cnt += 1
        
        # if dead_cnt == 8:
        #     to_be_removed.append((i, j))

    #print(special_handling_set)
    # special handling indicates that a number cell has satisfied all its conditions
    # i this 
    for x, y in special_handling_set:
        # if a previously numbered cell becomes 0
        # then it cannot have any new flags
        for nx, ny in getNeighbors(x, y):
            if board[nx][ny].value == "9":
                # any open cell nearby cannot be flagged
                board[nx][ny].value = "0"


  
            
pos = 0

def force(RADIUS, red_tar_x, red_tar_y):
    global window_origins, pos
    def _get_force_window(i, j):
        for x in range(i - RADIUS, i + RADIUS - 1):
            for y in range(j - RADIUS, j + RADIUS - 1):
                yield x, y 
    #print(one_set)
    numbers_strs = set(list("12345678"))
    for x, y in _get_force_window(red_tar_x, red_tar_y):
        """
        Check each cell in the window for any forces.
        """
        if board[x][y].value not in numbers_strs:
            continue
        
        # only now considering the cells with numberical values
        int_val = int(board[x][y].value) # 

        possibilities = []
        for nx, ny in getNeighbors(x, y):
            if board[nx][ny].value == "9":
                possibilities.append((nx, ny))
        
        #print(f"POS FOR {nx}, {ny} = {possibilities}")
        meta_board = {}

        if len(possibilities) == int_val:
            for ax, ay in possibilities:
                print(f"FOUND ONLY ONE POSSIBILITY FOR {ax}, {ay}")
                pos += 1

                if pos % 10000 == 0:
                    with open(f"gameboard{str(time())}.txt", "w+") as f:
                        for line in board:
                            f.write(f"{''.join([l.value for l in line]).replace('0', ' ')}\n")

                board[ax][ay] = Flag("X")
                unhandled_flags.add((ax, ay))
                saved_unhandled_flags.add((ax, ay))



                reduce() # fuck

        # with open(f"gameboard{str(time())}.txt", "w+") as f:
        #     for line in board:
        #         f.write(f"{''.join([l.value for l in line]).replace('0', ' ')}\n")



            #print(ax, ay)

             #early? very slow unfortunately


from sklearn.cluster import DBSCAN
import numpy as np

def merge_cells(window_origins, distance):
    try:
        # Convert the list of cells to a numpy array
        cells_array = np.array(window_origins)
        if len(cells_array.shape) == 1:
            cells_array = cells_array.reshape(-1, 1)

        dbscan = DBSCAN(eps=distance, min_samples=2)

        labels = dbscan.fit_predict(cells_array)

        merged_cells = {}

        for label, cell in zip(labels, window_origins):
            # If the label is -1, it represents noise and will be ignored
            if label == -1:
                continue
            if label not in merged_cells:
                merged_cells[label] = cell
            else:
                merged_cells[label] = [(x + y) // 2 for x, y in zip(merged_cells[label], cell)]
        return list(merged_cells.values())

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Return the original array if an error occurs
        return window_origins



i = 0
from time import time

start = True
while unhandled_flags:
    print("BEGIN REDUCE")
    reduce()
    print("END REDUCE")

    original_len = len(window_origins)
    window_origins = merge_cells(list(window_origins), 2) # is it rly worth?


    print(f"BEGIN {len(window_origins)} FORCES WITH RADIUS {20}, REDUCED FROM {original_len}")
    
    while window_origins:
        x, y = window_origins.pop()
        force(20, x, y)
    

    print("FINISHED FORCE")

    # now reset  unhandled_flags?
    unhandled_flags = saved_unhandled_flags.copy()
    
    
    i += 1

    if i % 5 == 1:
        with open(f"gameboard{str(time())}.txt", "w+") as f:
            for line in board:
                f.write(f"{''.join([l.value for l in line]).replace('0', ' ')}\n")

with open(f"gameboard{str(time())}.txt", "w+") as f:
    for line in board:
        f.write(f"{''.join([l.value for l in line]).replace('0', ' ')}\n")

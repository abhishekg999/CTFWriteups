from z3 import *

with open("gameboard.txt", "r") as fin:
    circuit = fin.read()
    circuit = circuit.replace(" ", "0")
    circuit = [list(line) for line in circuit.split("\n")]

print(len(circuit), len(circuit[0]))

board = []
variable_set = set()
interest_pnt = list()
for x, line in enumerate(circuit):
    inner_row = []
    for y, cell in enumerate(line):
        if cell == "B":
            inner_row.append("B")

        elif cell == "9":
            sym_var = Int(f"C{x}_{y}")
            variable_set.add(sym_var)
            inner_row.append(sym_var)

        elif cell != "0":
            # 1-8
            interest_pnt.append((x, y))
            inner_row.append(cell)
        else:
            inner_row.append(cell)

    board.append(inner_row)

print(f"Initialized board with {len(variable_set)} variables")


def getNeighbors(i, j):
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if x == i and y == j:
                continue
            yield x, y


solver = Solver()
for cell in variable_set:
    solver.add(Or(cell == 0, cell == 1))

numbers_limits = set(list("12345678"))
for x, y in interest_pnt:
    value = int(board[x][y])
    dec = 0
    candidates = []
    for nx, ny in getNeighbors(x, y):
        if type(board[nx][ny]) != str:
            candidates.append(board[nx][ny])

        else:
            assert isinstance(board[nx][ny], str)
            if board[nx][ny] == "B":
                dec += 1

    if candidates:
        solver.add(Sum(candidates) == value - dec)

print("ADDED ALL EQUATIONS")

if solver.check() == sat:
    model = solver.model()
    with open("model.txt", "w") as file:
        file.write(model.sexpr())
    print(model)
    
else:
    print("unsat")

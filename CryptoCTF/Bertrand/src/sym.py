import functools
from PIL import Image
from z3 import *

key = "k3Y"
n = 256

def sox(n, d):
	x, y, t = 0, 0, d
	for s in range(n - 1):
		u = 1 & t // 2
		v = 1 & t ^ u
		x, y = spin(2**s, x, y, u, v)
		x += 2**s * u
		y += 2**s * v
		t = t // 4
	return x, y

def spin(n, x, y, u, v):
	if v == 0:
		if u == 1:
			x = n - 1 - x
			y = n - 1 - y
		x, y = y, x
	return x, y

import pickle

with open("hilbert.json", 'rb') as f:
	table = pickle.load(f)

buf = [Int(f"F_{i}") for i in range(n**2)]
def encrypt(_, key, n):
	_msg = buf
	_key = [ord(_) for _ in key]
	
	img = Image.open("enc.png")
	img = img.rotate(90)
	pix = img.load()

	actual_msg = [0 for _ in range(n**2)]

	for (x, y), v in table.items():
		actual_msg[v] = pix[x, y][0] 

	for _ in range(len(key)):
		w = len(_key)
		h = n**2 // w + 1
		arr = [[_msg[w*x + y] if w*x + y < n**2 else None for x in range(h)] for y in range(w)]
		_conf = sorted([(_key[i], i) for i in range(w)])
		_marshal = [arr[_conf[i][1]] for i in range(w)]
		_msg = functools.reduce(lambda a, r: a + _marshal[r], range(w), [])
		_msg = list(filter(lambda x: x is not None, _msg))

		_msg = [(_msg[_] + _key[_ % w]) % 256 for _ in range(n**2)]

		# new z3 solve
		solver = Solver()

		for sym, actual in zip(_msg, actual_msg):
			solver.add(sym == actual)
		
		for sym in buf:
			solver.add(sym > 32)
			solver.add(sym < 127)
	
	return solver
				
print("BUILDING EQUATION")
solver = encrypt(None, key, n)

print("SOLVING FOR SATISFYING FLAG")
if solver.check() == sat:
	m = solver.model()
	print(''.join(chr(m[b].as_long()) for b in buf))
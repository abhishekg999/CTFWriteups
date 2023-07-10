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

n = 256
def gen_hilbert_table():
	m = {}
	for i in range(n**2):
		t = sox(n, i)
		m[t] = i
	
	return m

import pickle

with open("hilbert.json", 'rb') as f:
	table = pickle.load(f)

from PIL import Image

img = Image.open("enc.png")
img = img.rotate(90)
pix = img.load()

_msg = [0 for _ in range(n**2)]

for (x, y), v in table.items():
	_msg[v] = pix[x, y][0] 

#print(_msg)

l = [4854, 14563, 31553, 43690, 55826]
msg = 'CCTF{'

header = [_msg[i] for i in l]
print(header)

from shift_solvers import solve_key_4, m4_shift_back
from z3 import *
def m4_shift_back(a):
	shift = [0, 1, 2, 4, 3]
	return [a[s] for s in shift]

def solve_key_4(ct_fixed, pt):
	print(pt)
	print(ct_fixed)
	solver = Solver()
	vars = [Int(f'k_{x}') for x in range(3)]
	k0, k1, k2 = vars

	N = 256
	solver.add(k0 > 0, k1 > 0, k2 > 0)
	solver.add(k0 < 256, k1 < 256, k2 < 256)
	solver.add(ct_fixed[0] == (pt[0] + 2*k1 + k2) % N)
	solver.add(ct_fixed[1] == (pt[1] + 2*k1 + k2) % N)
	solver.add(ct_fixed[2] == (pt[2] + 3*k0) % N)
	solver.add(ct_fixed[3] == (pt[3] + 2*k0 + k2) % N)
	solver.add(ct_fixed[4] == (pt[4] + 2*k1 + k2) % N)
	
	while solver.check() == sat:
		m = solver.model()
		print(m)
		print("".join(chr(m[x].as_long()) for x in reversed(vars)))
	
		solver.add(Or(k0 != m[k0], k1 != m[k1], k2 != m[k2]))


s = solve_key_4(m4_shift_back(header), [ord(x) for x in msg])
print(s)

img.close()

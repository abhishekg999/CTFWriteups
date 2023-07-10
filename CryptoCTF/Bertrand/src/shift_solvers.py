from z3 import *

def m0_shift_back(a):
	shift = [0, 3, 2, 1, 4]
	return [a[s] for s in shift]

def solve_key_0(ct_fixed, pt):
	print(pt)
	print(ct_fixed)
	
	solver = Solver()
	vars = [Int(f'k_{x}') for x in range(3)]
	k0, k1, k2 = vars

	N = 256
	solver.add(k0 >= 0, k1 >= 0, k2 >= 0)
	solver.add(k0 < 128, k1 < 128, k2 < 128)
	solver.add(ct_fixed[0] == (pt[0] + 3*k2) % N)
	solver.add(ct_fixed[1] == (pt[1] + k1 + 2*k2) % N)
	solver.add(ct_fixed[2] == (pt[2] + 2*k0 + k2) % N)
	solver.add(ct_fixed[3] == (pt[3] + 2*k1 + k2) % N)
	solver.add(ct_fixed[4] == (pt[4] + 3*k1) % N)
	
	print(solver.check())
	assert solver.check() == sat
	m = solver.model()
	print(m)

	print("".join(chr(m[x].as_long()) for x in reversed(vars)))

def m1_shift_back(a):
	shift = [4, 3, 2, 1, 0]
	return [a[s] for s in shift]

def solve_key_1(ct_fixed, pt):
	solver = Solver()
	vars = [Int(f'k_{x}') for x in range(3)]
	k0, k1, k2 = vars

	N = 256
	solver.add(k0 > 0, k1 > 0, k2 > 0)
	solver.add(k0 < 128, k1 < 128, k2 < 128)
	solver.add(ct_fixed[0] == (pt[0] + k0 + k1 + k2) % N)
	solver.add(ct_fixed[1] == (pt[1] + k0 + k1 + k2) % N)
	solver.add(ct_fixed[2] == (pt[2] + k1 + 2*k2) % N)
	solver.add(ct_fixed[3] == (pt[3] + 2*k0 + k1) % N)
	solver.add(ct_fixed[4] == (pt[4] + k0 + k1 + k2) % N)
	
	while solver.check() == sat:
		m = solver.model()
		print(m)
		print("".join(chr(m[x].as_long()) for x in reversed(vars)))
	
		solver.add(Or(k0 != m[k0], k1 != m[k1], k2 != m[k2]))


def m2_shift_back(a):
	shift = [0, 4, 3, 2, 1]
	return [a[s] for s in shift]

def solve_key_2(ct_fixed, pt):
	print(pt)
	print(ct_fixed)
	solver = Solver()
	vars = [Int(f'k_{x}') for x in range(3)]
	k0, k1, k2 = vars

	N = 256
	solver.add(k0 > 0, k1 > 0, k2 > 0)
	solver.add(k0 < 256, k1 < 256, k2 < 256)
	solver.add(ct_fixed[0] == (pt[0] + 3*k2) % N)
	solver.add(ct_fixed[1] == (pt[1] + k0 + k1 + k2) % N)
	solver.add(ct_fixed[2] == (pt[2] + k0 + k1 + k2) % N)
	solver.add(ct_fixed[3] == (pt[3] + k0 + 2*k1) % N)
	solver.add(ct_fixed[4] == (pt[4] + k0 + 2*k2) % N)
	
	while solver.check() == sat:
		m = solver.model()
		print(m)
		print("".join(chr(m[x].as_long()) for x in reversed(vars)))
	
		solver.add(Or(k0 != m[k0], k1 != m[k1], k2 != m[k2]))

def m3_shift_back(a):
	shift = [4, 3, 2, 1, 0]
	return [a[s] for s in shift]

def solve_key_3(ct_fixed, pt):
	print(pt)
	print(ct_fixed)
	solver = Solver()
	vars = [Int(f'k_{x}') for x in range(3)]
	k0, k1, k2 = vars

	N = 256
	solver.add(k0 > 0, k1 > 0, k2 > 0)
	solver.add(k0 < 256, k1 < 256, k2 < 256)
	solver.add(ct_fixed[0] == (pt[0] + 2*k0 + k2) % N)
	solver.add(ct_fixed[1] == (pt[1] + 2*k0 + k2) % N)
	solver.add(ct_fixed[2] == (pt[2] + k0 + k1 + k2) % N)
	solver.add(ct_fixed[3] == (pt[3] + 3*k2) % N)
	solver.add(ct_fixed[4] == (pt[4] + k0 + k1 + k2) % N)
	
	while solver.check() == sat:
		m = solver.model()
		print(m)
		print("".join(chr(m[x].as_long()) for x in reversed(vars)))
	
		solver.add(Or(k0 != m[k0], k1 != m[k1], k2 != m[k2]))


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

		
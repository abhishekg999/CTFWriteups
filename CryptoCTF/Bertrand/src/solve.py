import string
from random import randint
import functools

def pad(s, l):
	while len(s) < l:
		s += string.printable[randint(0, 61)]
	return s

def padd(s, l, d):
	while len(s) < l:
		s += d
	return s


def do(n, msg, key, sl=None):
	_msg = padd(msg, n**2, '\0')
	_msg, _key = [ord(_) for _ in _msg], [ord(_) for _ in key]
	for _ in range(len(key)):
		w = len(_key)
		h = n**2 // w + 1
		arr = [[_msg[w*x + y] if w*x + y < n**2 else None for x in range(h)] for y in range(w)]

		if not sl:
			_conf = sorted([(_key[i], i) for i in range(w)])
		else:
			_conf = sorted([(_key[i], i, sl[i]) for i in range(w)], key=lambda x: x[2])

		_marshal = [arr[_conf[i][1]] for i in range(w)]
		_msg = functools.reduce(lambda a, r: a + _marshal[r], range(w), [])
		_msg = list(filter(lambda x: x is not None, _msg))
		_msg = [(_msg[_] + _key[_ % w]) % 256 for _ in range(n**2)]

	return _msg



n = 256
msg = 'ABCDE'

TEMP = '\1\2\3'
baseline = do(n, msg, '\0\0\0', TEMP)
base = []
l = []
for i, v in enumerate(baseline):
	if v > 1:
		base.append((i, chr(v)))
		l.append(i)
print(base)
print(l)
print('------------------------')
diffs = []

for key in ['\x00\x00\x00', '\x00\x00\x01', '\x00\x01\x00', '\x01\x00\x00']:
	n = 256
	msg = 'CCTF{'

	baseline = do(n, msg, key, TEMP)
	idk = [baseline[i] for i in l]
	print(idk)

	diffs.append(idk)

for p, f in zip(diffs, [diffs[0]]*len(diffs)):
	print([p[i] - f[i] for i in range(len(p))])

"""
c0 = 3k_2
c1 = k_1 + 2k_2
c2 = 2k_0 + k_2
c3 = 2k_1 + k_2
c4 = 3k_1
"""
from shift_solvers import solve_key_0, m0_shift_back
from shift_solvers import solve_key_1, m1_shift_back
from shift_solvers import solve_key_2, m2_shift_back
from shift_solvers import solve_key_3, m3_shift_back
from shift_solvers import solve_key_4, m4_shift_back

key = "\3\1\2"
n = 256
msg = 'CCTF{'

q = do(n, msg, key)
header = [q[i] for i in l]

print('------')


s = solve_key_4(m4_shift_back(header), [ord(x) for x in msg])
print(s)




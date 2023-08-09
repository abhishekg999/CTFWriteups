import re

regex_pattern = r'C23_(\d+).......\n..(.)'

with open('model.txt', 'r') as file:
    content = file.read()

result_dict = {}
matches = re.findall(regex_pattern, content)

for match in matches:
    key = int(match[0]) 
    value = int(match[1]) 
    result_dict[key] = value

bits = [0 for _ in range(3600)]

for x in result_dict:
    bits[x] = result_dict[x]

import hashlib
flag = hashlib.sha256(bytes(bits)).hexdigest()
print(f'Flag: CTF{{{flag}}}')
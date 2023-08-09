from PIL import Image

image = Image.open("symatrix.png")
matrix = image.load()

(x_len, y_len) = image.size
print(x_len, y_len)

o_len = (x_len + 1) // 2
nx_len = (o_len * 2) - 1

different_pixels = []
for i in range(y_len):
    for j in range(o_len):
        pixel = matrix[j, i]
        if matrix[nx_len - j, i] != matrix[j, i]:
            different_pixels.append((matrix[nx_len - j, i], matrix[j, i]))

for pixel_pair in different_pixels:
    print(f"{pixel_pair[0]}, {pixel_pair[1]}")

import binascii

binary_string = ''.join([str(p[0][2]) for p in different_pixels])
hex_string = hex(int(binary_string, 2))[2:]
decoded_data = binascii.unhexlify(hex_string).decode('utf-8')

print(decoded_data)
from PIL import Image
from random import randint
import binascii          
       
# def hexstr_to_binstr(hexstr):           
#     n = int(hexstr, 16)
#     n = int(hexstr, 16)
#     bstr = ''
#     bstr = ''

def hex_to_binary(hex_string):
    decimal_number = int(hex_string, 16)  # Convert hex string to decimal number
    binary_string = bin(int(hex_string, 16))[2:]  # Convert decimal number to binary string
    return binary_string

def pixel_bit(b):       
    return tuple((0, 1, b))

def embed(t1, t2): 
    return tuple((t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2]))

def full_pixel(pixel):         
    return pixel[1] == 255 or pixel[2] == 255

bin_data = open("./flag.txt", 'rb').read()        
data_to_hide = binascii.hexlify(bin_data).decode('utf-8')
binary_string = hexstr_to_binstr(data_to_hide)

base_image = Image.open("./original.png")           


x_len, y_len = base_image.size
nx_len = x_len * 2

new_image = Image.new("RGB", (nx_len, y_len))

base_matrix = base_image.load()
new_matrix = new_image.load()

binary_string = hexstr_to_binstr(data_to_hide)
remaining_bits = len(binary_string)

nx_len = nx_len - 1
next_position = 0           

for i in range(0, y_len):
    for j in range(0, x_len):
        pixel = new_matrix[j, i] = base_matrix[j, i]            
        if remaining_bits > 0 and next_position <= 0 and not full_pixel(pixel):
            new_matrix[nx_len - j, i] = embed(pixel_bit(int(binary_string[0])),pixel)
            next_position = randint(1, 17)
            binary_string = binary_string[1:]            
            remaining_bits -= 1
        else:
            new_matrix[nx_len - j, i] = pixel           
            next_position -= 1

new_image.save("./symatrix.png")            
new_image.close()
 
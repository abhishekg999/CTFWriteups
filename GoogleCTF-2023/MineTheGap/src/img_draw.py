from PIL import Image, ImageDraw

CELL_SIZE = 18

textures = {
    'flag': "img/flag.png",
    'cell0': "img/cell0.png",
    'cell1': "img/cell1.png",
    'cell2': "img/cell2.png",
    'cell3': "img/cell3.png",
    'cell4': "img/cell4.png",
    'cell5': "img/cell5.png",
    'cell6': "img/cell6.png",
    'cell7': "img/cell7.png",
    'cell8': "img/cell8.png",
    'closed': "img/cell_close.png"
}

# Dictionary to store loaded and resized texture images
texture_images = {}

def load_texture_images():
    for key, path in textures.items():
        texture_image = Image.open(path)
        texture_image = texture_image.resize((CELL_SIZE, CELL_SIZE))
        texture_images[key] = texture_image

def draw_image_from_array(array):
    width = len(array[0]) * CELL_SIZE
    height = len(array) * CELL_SIZE

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    for row in range(len(array)):
        print(row)
        for col in range(len(array[row])):
            texture_key = get_texture(array[row][col])

            if texture_key == 'img/cell0.png':
                continue
            texture_image = texture_images.get(texture_key, texture_images['closed'])

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            image.paste(texture_image, (x, y))

    return image

def get_texture(key):
    if key == 'X':
        key = 'B'
        
    state = int(key, 16)
    if state in range(0, 9):
        return f'cell{state}'
    elif state == 9:
        return 'closed'
    elif state == 10: # Chosen mine
        return 'flag'
    elif state == 11: # Fixed mine
        return 'flag'

# Load and resize the texture images
load_texture_images()

import sys
img = sys.argv[1]

with open(img, 'r') as fin:
    circuit = fin.read()
    circuit = circuit.replace(' ', '0')
    circuit = [list(line) for line in circuit.split('\n') if len(line) > 0]

result_image = draw_image_from_array(circuit)
result_image.save(f"im_{img}.png")

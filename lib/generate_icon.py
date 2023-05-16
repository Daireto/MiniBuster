from PIL import Image
image = Image.open('../minibuster.ico')

mode = image.mode
size = image.size
pixels = list(image.getdata())

with open('image.py', 'w') as f:
    f.seek(0)
    f.truncate()
    f.write(f'mode = \'{mode}\'\n')
    f.write(f'size = {size}\n')
    f.write(f'pixels = {pixels}')

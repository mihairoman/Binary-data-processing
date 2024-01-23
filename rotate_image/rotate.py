# https://en.wikipedia.org/wiki/BMP_file_format#DIB_header_(bitmap_information_header)  
# import struct

with open('./test/teapot.bmp', 'rb') as file:
    data = file.read()

# Use struct.unpack or little_endian function to get the following values:
# pixel_array_offset = struct.unpack('<I', data[10:14])[0] # offset 10, 4 bytes
# pixel_array_width = struct.unpack('<I', data[18:22])[0] # offset 18, 4 bytes
# pixel_array_height = struct.unpack('<I', data[22:26])[0] # offset 22, 4 bytes

def little_endian(bytes):
    acc = 0
    for i, byte in enumerate(bytes):
        acc += (byte << (i * 8))
    return acc

offset, width, height = little_endian(data[10:14]), little_endian(data[18:22]), little_endian(data[22:26])

rotated_img = [[None]*height for _ in range(width)]

"""
In an image of width w and with a pixel at coordinates (x, y), 
the pixel's RGB values would be stored at bytes 
3*(y*w + x), 3*(y*w + x) + 1, and 3*(y*w + x) + 2 in the pixel data.
"""
for y in range(height):
    for x in range(width):
        new_x = y
        new_y = width - x - 1
        pixel_offset = (y * width + x) * 3
        pixel = data[offset + pixel_offset: offset + pixel_offset + 3]
        rotated_img[new_y][new_x] = pixel

# Flatten the rotated image into a 1D list
rotated_img_flat = [pixel for row in rotated_img for pixel in row]

with open('./test/out.bmp', 'wb') as file:
    file.write(data[:offset])
    file.write(b''.join(rotated_img_flat))

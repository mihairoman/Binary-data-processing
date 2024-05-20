import sys

"""
Truncate a UTF-8 string to a given length in bytes.

UTF-8 says to start with number of 1 bits which tells how many bytes 
we will use to encode the code point, then a 0. Which is followed by payload bits.
The second byte starts with “1 0” to distinguish the non-beginning of a byte sequence 
from any valid beginning of a byte sequence.

1 1 0 . . . .      1 0 . . . . . .
1 1 1 0 . . .      1 0 . . . . . .    1 0 . . . . . .
1 1 1 1 0 . . .    1 0 . . . . . .    1 0 . . . . . .    1 0 . . . . . . 
"""

def truncate(string: str, length: int) -> str:
    if length >= len(string):
        return string
    # if the byte at location is a continuation byte, we need to go back until we find the start of the character
    while length > 0 and (string[length] & 0b11000000) == 0b10000000:
        length -= 1
    return string[:length]

with open('assets/cases', 'rb') as file:
   while True:
    line = file.readline()

    if not len(line):
        break

    length_to_truncate = line[0]
    string = line[1:-1] # skip first and last byte (length to truncate and newline)
    sys.stdout.buffer.write(truncate(string, length_to_truncate) + b'\n') 
    
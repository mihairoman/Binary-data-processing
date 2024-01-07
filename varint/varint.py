import struct

## https://protobuf.dev/programming-guides/encoding/#varints

def encode(number):
    """
    while n > 0:
        get lowest 7 bits of number: &0b01111111 (or number % 128; 128 = 2^7)
        add the 1 to the msb if it's not last processed byte (|= 0b10000000 or |= 0x80 or |= 128)
        append to byte array
        reduce n by 7 bits
    return byte array
    """
    output = bytearray()
    while number > 0:
        lowest_7_bits = number & 0x7F
        number >>= 7
        if number > 0:
            lowest_7_bits |= 0x80 
        output.append(lowest_7_bits)
    return output

def decode(varn):
    """
    for byte in varn in reverse order:
        shift number by 7 bits (disregard the msb)
        add byte to number
    return number
    """
    output = 0
    for byte in reversed(varn):
       output <<= 7 
       output |= byte
    return output

if __name__ == '__main__':
    cases = (
        ('./test/1.uint64', b'\x01'),
        ('./test/150.uint64', b'\x96\x01'),
        ('./test/maxint.uint64', b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01'),
    )
    
    for fname, expectaction in cases: 
        with open(fname, 'rb') as f:
            number = struct.unpack('>Q', f.read())[0]
            assert encode(number) == expectaction
            assert decode(encode(number)) == number
    print('All tests passed.')

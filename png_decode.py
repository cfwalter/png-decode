#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
import sys

def read_chunk(fin):
    chunk_size = fin.read(4)
    chunk_type = fin.read(4)
    try:
        data_length = struct.unpack('>i', chunk_size)[0]
    except:
        print(chunk_type)
        return

    data = fin.read(data_length)
    crc = fin.read(4)
    return {
        'data': data,
        'type': chunk_type,
        'length': chunk_size,
        'crc': crc,
    }

def read_pixel(data):
    print(data)
    pass


def write_chunk(fout, chunk):
    fout.write(chunk['length'])
    fout.write(chunk['type'])
    fout.write(chunk['data'])
    fout.write(chunk['crc'])


def main(file_name):
    fin = open(file_name, 'rb')
    fout = open('out.png', 'wb')
    header = fin.read(8)
    if header != b'\x89PNG\r\n\x1a\n':
        print('Not a PNG file!')
        return

    fout.write(header)

    IHDR = read_chunk(fin)
    bit_depth = list(IHDR['data'])[8]
    color_type = list(IHDR['data'])[9]

    new_ihdr = list(IHDR['data'])
    # we're making it greyscale
    new_ihdr[9] = 4
    IHDR['data'] = bytearray(new_ihdr)

    write_chunk(fout, IHDR)

    for i in range(32):
        chunk = read_chunk(fin)
        write_chunk(fout, chunk)
    #     # if chunk['type'] == b'IDAT':
    #     #     print(chunk['type'], len(chunk['data']),)
    #     #     for i in range(0, len(chunk['data']), 32):
    #     #         read_pixel(chunk['data'][i:i+32])

        if chunk['type'] == b'IEND':
            break


if __name__ == "__main__":
    main(sys.argv[1])

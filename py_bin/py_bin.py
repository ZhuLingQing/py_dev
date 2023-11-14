import sys
import struct
import os
import math

__endian = 'little'

def isPowerOfTwo(num : int):
    if math.log(num,2).is_integer():
        return True
    else:
        return False

def reaadBinFile(file_path):
    try:
        binfile = open(file_path,'rb')
        size = os.path.getsize(file_path)
        data = binfile.read(size)
        #data = []
        #for i in range(size):
        #    data.append(binfile.read(1))
        binfile.close()
        return data
    except:
        assert False, "file not exist"

def writeBinFile(file_path, bary):
    try:
        binfile = open(file_path,'wb')
        binfile.write(bary)
        binfile.close()
    except:
        assert False, "file not exist"


def convert16to4(bin_ary):
    l4 = []
    for i in range(0, len(bin_ary), 4):
        assert bin_ary[i + 1] == 0 and bin_ary[i + 3] == 0, "invalid input buffer"
        temp = bin_ary[i] + (bin_ary[i + 2] * 16)
        print("%02x %02x %02x %02x >> %02x" % (bin_ary[i],bin_ary[i+1],bin_ary[i+2],bin_ary[i+3], temp))
        l4.append(temp)
    return bytes(l4)

def __max(a, b):
    if a >= b:
        return a
    return b

def __convertBytesToList(bin_ary : bytes, bit_width : int):
    l = []
    assert isPowerOfTwo(bit_width), "invalid bit width"
    __mask = (1 << bit_width) - 1
    num_of_bytes = int(bit_width / 8)
    if 0 == num_of_bytes:
        for a in bin_ary:
            x = a
            for shift in range(0, 8, bit_width):
                l.append(x & __mask)
                x >>= bit_width
    else:
        assert len(bin_ary) % num_of_bytes == 0, "invalid binary size"
        for i in range(0, len(bin_ary), num_of_bytes):
            temp = int.from_bytes(bin_ary[i:i+num_of_bytes], byteorder=__endian, signed=False)
            #l.append(list(temp.to_bytes(num_of_bytes,__endian)))
            l.append(temp)
    return l

def __convertListToBytes(data_l : list, bit_width : int):
    bary = bytearray()
    assert isPowerOfTwo(bit_width), "invalid bit width"
    __mask = (1 << bit_width) - 1
    num_of_bytes = int(bit_width / 8)
    if 0 == num_of_bytes:
        for i in range(0, len(data_l), int(8/bit_width)):
            b = 0
            for n in range(int(8/bit_width) - 1, -1, -1):
                b <<= bit_width
                temp = data_l[i + n] & __mask
                assert temp == data_l[i + n], "invalid input, high bit data may lost"
                b += temp
            assert b & 0xFF == b, "invalid input, high bit data may lost"
            bary += b.to_bytes(1,__endian)
    else:
        for b in data_l:
            bary += b.to_bytes(num_of_bytes,__endian)
    return bary

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("arg1: file path name")
        print("arg2: %%d(from):%%d(to)")
        sys.exit(1)
    fname_i = sys.argv[1]
    format_c = sys.argv[2].split(':')
    assert len(format_c) == 2 and format_c[0].isdigit() and format_c[1].isdigit(), "invalid arg2"
    from_i = int(format_c[0])
    to_i = int(format_c[1])
    assert (from_i % to_i) == 0, "invalid arg2"
    fname_o = fname_i[0:len(fname_i) - 4] + str.format("_%dto%d.bin" % (from_i, to_i))
    in_b = reaadBinFile(fname_i)
    in_l = __convertBytesToList(in_b, from_i)
    print("in : %s = %d" % (in_l[0:256], len(in_l)))
    out_b = __convertListToBytes(in_l, to_i)
    #print("out: %s = %d" % (out_b[0:256], len(out_b)))
    out_l = list(out_b)
    print("out: %s = %d" % (out_l[0:256], len(out_l)))
    #print("input: ", b16.hex())
    #out_b = convert_binary(in_b, from_i, to_i)
    #print("output: ", b4.hex())
    writeBinFile(fname_o, out_b)
    print("output to: %s " % (fname_o))
    print(" >>>>> done <<<<<")
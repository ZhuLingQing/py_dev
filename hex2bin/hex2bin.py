#!/usr/bin/python3

import sys, os
import numpy as np
import re
import subprocess
import shlex
import argparse

p = r"name=([0-9a-zA-Z_]+)\s+start_address=([0-9a-fA-Fx]+)\s+bytes=([0-9]+)\s+bytes_total=([0-9]+).*"
value_map = {'0': 0, '1': 1, '2':2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

def hexstr2bytelist(hexstr):
    assert hexstr.startswith("0x")
    a = hexstr
    a = a[2:]
    result = []
    while len(a) > 0:
        assert len(a) % 2 == 0
        bytestr = a[0:2]
        val = value_map[bytestr[1]]
        val += value_map[bytestr[0]] * 16
        result.insert(0, val)
        a = a[2:]
    return result

def hexstr2int(hexstr):
    assert hexstr.startswith("0x")
    a = hexstr[2:]
    result = 0
    while len(a) > 0:
        result *= 16
        result += value_map[a[0]]
        a = a[1:]

    return result

def decstr2int(decstr):
    a = decstr[:]
    result = 0
    while len(a) > 0:
        result *= 10
        result += value_map[a[0]]
        a = a[1:]

    return result

def __hex2bin(hex_path : str, bin_path : str = None):
    start_address = None
    current_address = None
    bin_content = []

    with open(hex_path, "r") as fhex:
        lines = fhex.readlines()
        for line in lines:
            if line.startswith("name"):

                m = re.match(p, line)
                assert m is not None
                name = m.group(1)
                start_address = m.group(2)
                bw = m.group(3)
                bytes_total = m.group(4)

                start_address = hexstr2int(start_address)
                bw = decstr2int(bw)
                bytes_total = decstr2int(bytes_total)
                gap = 0
                if current_address is not None:
                    gap = start_address - current_address
                assert gap >= 0, gap
                bin_content += [0] * gap
                current_address = start_address
                
            elif line.startswith("0x"):
                line_content = hexstr2bytelist(line.strip())
                bin_content += line_content
                assert current_address is not None
                current_address += len(line_content)
            else:
                assert False
    if (start_address % 64) != 0:
        bin_content = [0] * (start_address % 64) + bin_content
        start_address -= (start_address % 64)
    if (len(bin_content) % 64) != 0:
        bin_content = bin_content + [0] * (64 - (len(bin_content) % 64))
    b = bytearray(bin_content)
    if bin_path != None:
        with open(bin_path, "ab+") as f:
            f.write(b)
            f.close()
    return len(b)

sumb = 0
lBinSize = []
lBinOffset = []

def hex2bin(hex_path : str, bin_path : str, recursive = False):
    global sumb
    if os.path.isfile(hex_path):
        if hex_path[-4:] == '.hex':
            l = __hex2bin(hex_path, bin_path)
            print("%-100s %10d %08x"%(hex_path, l, (sumb)))
            lBinSize.append(l)
            lBinOffset.append(sumb)
            sumb += l
    elif os.path.isdir(hex_path):
        lFile = os.listdir(sys.argv[1])
        lFile.sort()
        for f_hex in lFile:
            hex_sub_path = hex_path + f_hex
            if os.path.isfile(hex_sub_path):
                hex2bin(hex_sub_path, bin_path)
            elif os.path.isdir(hex_sub_path) and recursive == None: # recursive nars==0, so None means True
                hex2bin(hex_sub_path, bin_path)
            else:
                print(hex_sub_path, " NOT EXIST")
                assert False
    else:
        print(hex_path, " NOT EXIST")
        assert False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=str, default=sys.argv[1])
    parser.add_argument('--outfile', '-o', type=str, default=sys.argv[1]+".bin")
    parser.add_argument('-r', '--recursive' , type=bool, default=False ,help='output file name, default = input + .bin', nargs='?')
    args = parser.parse_args()
    print([args.infile,args.outfile,args.recursive])
    try:
        os.remove(args.outfile + ".tmp")
    except:
        print("ready")
    sumb = 0
    hex2bin(args.infile, args.outfile + ".tmp", args.recursive)
    print("size:", lBinSize , len(lBinSize))
    print("offset:", lBinOffset , len(lBinOffset))
    print("Total size:", sumb)
    os.rename(args.outfile + ".tmp", args.outfile)


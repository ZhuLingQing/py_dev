from ctypes import *
import sys
import struct
import os

__README = '''
  This script is used to add signature for gf_aurora image.
It utilized ctypes for converting  between c structure and python class.
'''

def read_bin(file_path):
    try:
        binfile = open(file_path,'rb')
        size = os.path.getsize(file_path)
        data = binfile.read(size)
        binfile.close()
        return data
    except:
        assert False, "file not exist"

def write_bin(file_path, bary):
    try:
        binfile = open(file_path,'wb')
        binfile.write(bary)
        binfile.close()
    except:
        assert False, "file not exist"

def compute_checksum32(bary, seed : int = 0):
    assert len(bary) % 4 == 0, "invalid buffer for checksum32"
    for i in range(0, len(bary), 4):
        seed += int.from_bytes(bary[i:i+4], byteorder='little', signed=False)
    return seed & 0xFFFFFFFF

def find_argvalue(long_name : str, short_name : str = None):
    assert None == short_name or len(short_name) == 1, "invalid short_name"
    for i in range(1, len(sys.argv) - 1):
        arg = sys.argv[i]
        if arg[0:2] == '--' and arg[2:] == long_name: #long arg
            return sys.argv[i + 1]
        elif arg[0:1] == '-' and None != short_name and arg[1] == short_name[0]: #short arg
            return sys.argv[i + 1]
    return None

def find_arg(long_name : str, short_name : str = None):
    assert None == short_name or len(short_name) == 1, "invalid short_name"
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg[0:2] == '--' and arg[2:] == long_name: #long arg
            return sys.argv[i]
        elif arg[0:1] == '-' and None != short_name and arg[1] == short_name[0]: #short arg
            return sys.argv[i]
    return None


class GfAuroraWorkloadSign(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('name', c_char * 16),
        ('version', c_int32),
        ('checksum32', c_int32),
        ('size_in_bytes', c_int32),
        ('tag', c_char * 20),
        ('repo', c_char * 16),
        ('branch', c_char * 16),
    ]
    
    def encode(self):
        return string_at(addressof(self), sizeof(self))

    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__README)
        print("arg1: file name")
        print("optional args: --repo, --tag, --branch")
        sys.exit(1)
    fname_i = sys.argv[1]
    fname_s = fname_i.split('/')[-1].split('.')[0]
    #print(fname_s)
    fname_o = fname_i[0:len(fname_i) - 4] + "_sign.bin"
    in_b = read_bin(fname_i)
    sign = GfAuroraWorkloadSign()
    sign.decode(in_b)
    if len(sys.argv) == 2:
        chks = compute_checksum32(in_b)
        if 0 != chks:
            print("!!!!! invalid checksum (%x) !!!!!" % chks)
        else:
            print("name         :", sign.name.decode('utf-8'))
            print("checksum32   : 0x%x" % sign.checksum32)
            print("size_in_bytes:", sign.size_in_bytes)
            print("tag          :", sign.tag.decode('utf-8'))
            print("repo         :", sign.repo.decode('utf-8'))
            print("branch       :", sign.branch.decode('utf-8'))
    else:
        sign.name = bytes(fname_s, encoding = 'utf-8')
        sign.size_in_bytes = len(in_b)
        tag_s = find_argvalue("tag", 't')
        if None is not tag_s:
            sign.tag = bytes(tag_s, encoding = 'utf-8')
        repo_s = find_argvalue("repo", 'r')
        if None is not repo_s:
            sign.repo = bytes(repo_s, encoding = 'utf-8')
        branch_s = find_argvalue("branch", 'b')
        if None is not branch_s:
            sign.branch = bytes(branch_s, encoding = 'utf-8')
        sign.checksum32 = 0
        buf = sign.encode()
        chks = compute_checksum32(buf, 0)
        chks = compute_checksum32(in_b[len(buf):], chks)
        sign.checksum32 = ((~chks) & 0xFFFFFFFF) + 1
        print("checksum32 is: %x" % sign.checksum32)
        buf = sign.encode()
        out_b = buf + in_b[len(buf):]
        write_bin(fname_o, out_b)
        print("output to: ", fname_o)
    print(" >>>>> done <<<<<")
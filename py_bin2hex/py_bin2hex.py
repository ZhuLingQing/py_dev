import sys,os


def readBinFile(file_path):
    try:
        binfile = open(file_path,'rb')
        size = os.path.getsize(file_path)
        data = binfile.read(size)
        binfile.close()
        return data
    except:
        assert False, "file not exist"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("arg1: file path_name of binary")
        sys.exit(1)
    bin_path_name = sys.argv[1]
    bary = readBinFile(bin_path_name)
    print("The file has: ", len(bary))
    bin_path,bin_name = os.path.split(bin_path_name)
    hex_name = bin_name[0:-4]
    hex_path_name = bin_path_name[0:-4]
    hexfile = open(sys.argv[1][0:-4],'w')
    header = str.format("name=%s start_address=0x48000000000 bytes=1 bytes_total=%d\n" % (hex_name, len(bary)))
    hexfile.write(header)
    for i in range(0, len(bary)):
        dat = str.format("0x%02x\n" % bary[i])
        hexfile.write(dat)
    hexfile.close()
    print("output: ", hex_path_name)

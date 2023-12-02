import sys,os

def writeBinFile(file_path, bary):
    try:
        binfile = open(file_path,'wb')
        binfile.write(bary)
        binfile.close()
    except:
        assert False, "file not exist"

def readBinFile(file_path):
    try:
        binfile = open(file_path,'rb')
        size = os.path.getsize(file_path)
        data = binfile.read(size)
        binfile.close()
        return data
    except:
        assert False, "file not exist"

def __res50midProc(file_path):
    l_gap = 32
    l_size = (1605696, 401472, 401472, 401472, 1605696, 1605696, 401472, 401472, 1605696, 401472, 401472, 1605696, 802880, 200768, 802880, 802880, 200768, 200768, 802880, 200768, 200768, 802880, 200768, 200768, 802880, 401472, 100416, 401472, 401472, 100416, 100416, 401472, 100416, 100416, 401472, 100416, 100416, 401472, 100416, 100416, 401472, 100416, 100416, 401472, 200768, 50240, 200768, 200768, 50240, 50240, 200768, 50240, 50240, 200768, 4160, 2112)
    bary = readBinFile(file_path)
    baout = bytes()
    offset = 0
    for size in l_size:
        baout += b'\0'*l_gap #bytes([0]*l_gap)
        baout += bary[offset + l_gap : offset + size - 32]
        baout += b'\0'*l_gap #bytes([0]*l_gap)
        offset += size
    writeBinFile(file_path, baout)

if __name__ == "__main__":
    __res50midProc(sys.argv[1])
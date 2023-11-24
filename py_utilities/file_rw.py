import os

# write bytes into file
# return nunber of bytes written.
def writeBinFile(file_path, bary, append : bool = False):
    try:
        if append is True:
            binfile = open(file_path,'ab')
        else:
            binfile = open(file_path,'wb')
        binfile.write(bary)
        binfile.close()
        return len(bary)
    except:
        #assert False, "file not exist"
        return 0

# read bytes from file
# return bytes
def readBinFile(file_path):
    try:
        binfile = open(file_path,'rb')
        size = os.path.getsize(file_path)
        data = binfile.read(size)
        binfile.close()
        return data
    except:
        #assert False, "file not exist"
        return None
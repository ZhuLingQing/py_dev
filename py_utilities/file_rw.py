import os

# write bytes into file
# return nunber of bytes written.
def writeBinFile(file_path, bary, append : bool = False):
    try:
        if append is True:
            f = open(file_path,'ab')
        else:
            f = open(file_path,'wb')
        f.write(bary)
        f.close()
        return len(bary)
    except:
        #assert False, "file not exist"
        return 0

# read bytes from file
# return bytes
def readBinFile(file_path):
    try:
        f = open(file_path,'rb')
        size = os.path.getsize(file_path)
        data = f.read(size)
        f.close()
        return data
    except:
        #assert False, "file not exist"
        return None
    
def readTxtLines(file_path):
    with open(file_path, "r") as fhex:
        lines = fhex.readlines()
        fhex.close()
        return lines
    return None

def writeTxtLines(file_path, lines, append : bool = False):
    try:
        if append is True:
            f = open(file_path,'a')
        else:
            f = open(file_path,'w')
        for l in lines:
            f.write(l)
        f.close()
        return len(lines)
    except:
        #assert False, "file not exist"
        return 0
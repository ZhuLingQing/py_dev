import sys

_COLOR_DEFAULT_ = "\033[0m"
_COLOR_RED_ = "\033[31m"
_COLOR_GREEN_ = "\033[32m"

MAX_DIFF = 100

def bin_compare(bary1, bary2, line_size : int = 16):
    len_cmp = min([len(bary1), len(bary2)])
    offset = 0
    num_diff = 0
    while offset < len_cmp and num_diff < MAX_DIFF:
        ls_diff = []
        have_diff = False
        for i in range(0, line_size):
            if bary1[offset + i] != bary2[offset + i]:
                ls_diff.append(True)
                have_diff = True
                num_diff += 1
            else:
                ls_diff.append(False)
        if have_diff is True:
            print("%08X:" % offset),
            for i in range(0, line_size):
                if ls_diff[i] is True:
                    print(_COLOR_RED_),
                else:
                    print(_COLOR_DEFAULT_),
                print(bary1[offset + i].encode('hex')+_COLOR_DEFAULT_),
            print(" | "),
            for i in range(0, line_size):
                if ls_diff[i] is True:
                    print(_COLOR_RED_),
                else:
                    print(_COLOR_DEFAULT_),
                print(bary2[offset + i].encode('hex')+_COLOR_DEFAULT_),
            print("")
        offset += line_size
    print("%d/%d bytes compared done." % (offset,len_cmp)),
    if num_diff > 0:
        print(_COLOR_RED_+str.format("Found %d difference." % num_diff)+_COLOR_DEFAULT_)
    else:
        print(_COLOR_GREEN_+"Found no difference."+_COLOR_DEFAULT_)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("arg1 & arg2 are files to compare.")
        print("arg3 is number per line")
        sys.exit(1)
    
    with open(sys.argv[1],"rb") as f1, open(sys.argv[2],"rb") as f2:
        b1 = f1.read()
        b2 = f2.read()
        if len(sys.argv) == 4:
            bin_compare(b1, b2, int(sys.argv[3]))
        else:
            bin_compare(b1, b2)
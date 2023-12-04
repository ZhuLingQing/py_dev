import sys
import py_utilities.sh_color as sh_color

def bin_compare(bary1, bary2, line_size : int = 16, max_diff : int = 0):
    len_cmp = min([len(bary1), len(bary2)])
    offset = 0
    num_diff = 0
    while offset < len_cmp:
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
            print("%08X:" % offset, end=' ')
            for i in range(0, line_size):
                if ls_diff[i] is True:
                    print(sh_color.RED_B, end=' ')
                else:
                    print(sh_color.DEFAULT, end=' ')
                print(str.format("%02X" % bary1[offset + i])+sh_color.DEFAULT, end=' ')
            print(" | ", end=' ')
            for i in range(0, line_size):
                if ls_diff[i] is True:
                    print(sh_color.RED_B, end=' ')
                else:
                    print(sh_color.DEFAULT, end=' ')
                print(str.format("%02X" % bary2[offset + i])+sh_color.DEFAULT, end=' ')
            print("")
        offset += line_size
        if max_diff and num_diff >= max_diff:
            break
    print("%d/%d bytes compared done." % (offset,len_cmp), end=' ')
    if num_diff > 0:
        print(sh_color.RED_B+str.format("Found %d difference." % num_diff)+sh_color.DEFAULT)
    else:
        print(sh_color.GREEN_B+"Found no difference."+sh_color.DEFAULT)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("arg1 & arg2 are files to compare.")
        print("arg3 is number per line")
        print("arg4 is max difference")
        sys.exit(1)
    line_size = 16
    if len(sys.argv) >= 4:
        line_size = int(sys.argv[3])
    max_diff = 0
    if len(sys.argv) >= 5:
        max_diff = int(sys.argv[4])
    
    with open(sys.argv[1],"rb") as f1, open(sys.argv[2],"rb") as f2:
        b1 = f1.read()
        b2 = f2.read()
        bin_compare(b1, b2, line_size, max_diff)
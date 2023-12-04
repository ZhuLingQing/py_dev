import sys
import py_utilities.sh_color as sh_color

def bin_compare(bary1, bary2, break_on_diff : int = 0, disp_per_line : int = 0):
    len_cmp = min([len(bary1), len(bary2)])
    offset = 0
    num_diff = 0
    first_diff = None

    if disp_per_line > 0:
        while offset < len_cmp:
            ls_diff = []
            have_diff = False
            for i in range(0, disp_per_line):
                if bary1[offset + i] != bary2[offset + i]:
                    ls_diff.append(True)
                    have_diff = True
                    num_diff += 1
                    if first_diff is None:
                        first_diff = offset + i
                else:
                    ls_diff.append(False)
            if have_diff is True and disp_per_line != 0:
                print("%08X:" % offset, end=' ')
                for i in range(0, disp_per_line):
                    if ls_diff[i] is True:
                        print(sh_color.RED_B, end=' ')
                    else:
                        print(sh_color.DEFAULT, end=' ')
                    print(str.format("%02X" % bary1[offset + i])+sh_color.DEFAULT, end=' ')
                print(" | ", end=' ')
                for i in range(0, disp_per_line):
                    if ls_diff[i] is True:
                        print(sh_color.RED_B, end=' ')
                    else:
                        print(sh_color.DEFAULT, end=' ')
                    print(str.format("%02X" % bary2[offset + i])+sh_color.DEFAULT, end=' ')
                print("")
            offset += disp_per_line
            if break_on_diff and num_diff >= break_on_diff:
                break
        print("%d/%d bytes compared done." % (offset,len_cmp), end=' ')
        if num_diff > 0 and disp_per_line != 0:
            print(sh_color.RED_B+str.format("Found %d difference." % num_diff)+sh_color.DEFAULT)
        else:
            print(sh_color.GREEN_B+"Found no difference."+sh_color.DEFAULT)
    else:
        for i in range(0, len_cmp):
            if bary1[i] != bary2[i]:
                num_diff += 1
                if first_diff is None:
                    first_diff = i
                if break_on_diff and num_diff >= break_on_diff:
                    break
                
    return num_diff, first_diff

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("arg1 & arg2 are files to compare.")
        print("arg3 is max difference")
        print("arg4 is display column count per line")
        sys.exit(1)
    disp_per_line = 0
    if len(sys.argv) >= 5:
        disp_per_line = int(sys.argv[4])
    break_on_diff = 0
    if len(sys.argv) >= 4:
        break_on_diff = int(sys.argv[3])
    
    with open(sys.argv[1],"rb") as f1, open(sys.argv[2],"rb") as f2:
        b1 = f1.read()
        b2 = f2.read()
        num,first = bin_compare(b1, b2, disp_per_line, break_on_diff)
        if num == 0:
            print("No diff found.")
        else:
            print("%d diff found. First diff at 0x%X," % (num, first))
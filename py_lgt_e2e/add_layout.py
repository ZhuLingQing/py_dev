from py_utilities.file_rw import readTxtLines
from py_utilities.file_rw import writeTxtLines
import sys, os

start_index = 56
replace_num = 0

f_name = "/nfs/homes/tzhu/projects/pace2/model_zoo.50bc2/resnet50_batch2_dc/ops/resnet50_4pe.cpp"
f_out = f_name + ".bak"
l_in = readTxtLines(f_name)
l_out = []
for l in l_in:
    if l == "  CHECK_WEIGHT();\n":
        s = str.format("  CHECK_WEIGHT(%d);\n" % start_index)
        start_index += 1
        replace_num += 1
        l_out.append(s)
    else:
        l_out.append(l)

print("replaced %d, to %d" % (replace_num, start_index))
writeTxtLines(f_out, l_out)

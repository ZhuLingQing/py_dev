from py_utilities.file_rw import readTxtLines
from py_utilities.file_rw import writeTxtLines
import sys, os

start_index = 56
replace_num = 0

f_name = "/nfs/homes/tzhu/projects/pace2/model_zoo.50bc2/resnet50_batch2_dc/ops/resnet50_4pe.cpp"
f_out = f_name
l_in = readTxtLines(f_name)
l_out = []
line = 1
buf_index = 0
s_fmt = str.format("buf_%d, 1, " % buf_index)
for l in l_in:
    if l.find(s_fmt) != -1:
        t_fmt = str.format("buf_%d, BATCH_COUNT, " % buf_index)
        l = l.replace(s_fmt,t_fmt)
        print("line%d: %s" % (line, l), end='')
        buf_index += 1
        s_fmt = str.format("buf_%d, 1, " % buf_index)
    l_out.append(l)
    line += 1

print(buf_index)
writeTxtLines(f_out, l_out)

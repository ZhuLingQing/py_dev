import sys,os
import numpy as np
from py_utilities.file_rw import readTxtLines

def closestIndex(ls : list, num : int):
    answer = []
    for i in ls:
        answer.append(abs(num-i))
    return answer.index(min(answer))

fifo_len = 256
lut_len = 16

wgt_top_f = readTxtLines("wgt_top_f.txt")
wgt_top_0 = readTxtLines("wgt_top_0.txt")
wgt_btm_f = readTxtLines("wgt_btm_f.txt")
wgt_btm_0 = readTxtLines("wgt_btm_0.txt")

assert len(wgt_top_f) == fifo_len
assert len(wgt_top_0) == fifo_len
assert len(wgt_btm_f) == fifo_len
assert len(wgt_btm_0) == fifo_len

wgt_top_diff = []
wgt_btm_diff = []
for i in range(0,fifo_len):
    wgt_top_diff.append(int(wgt_top_f[i]) - int(wgt_top_0[i]))
    wgt_btm_diff.append(int(wgt_btm_f[i]) - int(wgt_btm_0[i]))

print("top diff:\n", wgt_top_diff, len(wgt_top_diff))
print("btm diff:\n", wgt_btm_diff, len(wgt_btm_diff))

top_min = min(wgt_top_diff)
top_max = max(wgt_top_diff)
print("top min:",top_min,", max:",top_max)
btm_min = min(wgt_btm_diff)
btm_max = max(wgt_btm_diff)
print("btm min:",btm_min,", max:",btm_max)

lut_space = np.linspace(min([top_min, btm_min]), max([top_max, btm_max]),lut_len)
print("lut_space:", lut_space)

lut_top = []
lut_top_val = []
for n in lut_space:
    index = closestIndex(wgt_top_diff, n)
    lut_top.append(index)
    lut_top_val.append(wgt_top_diff[index])
print("lut_top:", lut_top)
print("lut_top_val:", lut_top_val)

lut_btm = []
lut_btm_val = []
for n in lut_space:
    index = closestIndex(wgt_btm_diff, n)
    lut_btm.append(index)
    lut_btm_val.append(wgt_btm_diff[index])
print("lut_btm:", lut_btm)
print("lut_btm_val:", lut_btm_val)

lut_final = []
for i in range(0, lut_len):
    if abs(lut_space[i] - wgt_top_diff[lut_top[i]]) < abs(lut_space[i] - wgt_btm_diff[lut_btm[i]]):
        lut_final.append((lut_top[i], 0))
    elif abs(lut_space[i] - wgt_top_diff[lut_top[i]]) > abs(lut_space[i] - wgt_btm_diff[lut_btm[i]]):
        lut_final.append((0, lut_btm[i]))
    else: # if abs(lut_space[i], wgt_top_diff[lut_top[i]]) == abs(lut_space[i], wgt_btm_diff[lut_btm[i]]):
        if lut_top[i] <= lut_btm[i]:
            lut_final.append((lut_top[i], 0))
        else:
            lut_final.append((0, lut_btm[i]))
print("lut_final:", lut_final)


print(" >>> DONE <<<")
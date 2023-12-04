from py_utilities.file_rw import readTxtLines
from py_utilities.file_rw import readBinFile
from py_check.crc import crc16
import sys, os

kTotalLayers = 108
#tzhu:get script path
script_path = os.path.split(os.path.realpath(__file__))[0]
lines = readTxtLines(script_path+"/res50bc2_wgt_input_layout.txt")

#tzhu:3 columns: layer, offset, length
l_layer = []
l_offset = []
l_size = []
for l in lines:
    line = l.split(' ')
    l_layer.append(int(line[0]))
    l_offset.append(eval(line[1]))
    l_size.append(int(line[2]))
    #print (line, end=',')
#tzhu: get 3 lists: layer, offset, length
print("layer :", l_layer, len(l_layer))
print("offset:", l_offset, len(l_offset))
print("size  :", l_size, len(l_size))

#tzhu: get binary image
bary = readBinFile("/nfs/homes/tzhu/projects/pace2/model_zoo.50bc2/resnet50_batch2_dc/golden/m3_mqbench_qmodel_deploy_no_pot_scale.hex.bin")

assert len(l_layer) == kTotalLayers
assert len(l_offset) == kTotalLayers
assert len(l_size) == kTotalLayers

#tzhu: compute each layer's crc16 as result
l_crc = []
for layer in range(kTotalLayers):
    id = l_layer.index(layer)
    crc = crc16(bary[l_offset[id]:l_offset[id] + l_size[id]])
    #tzhu: combine crc16+image_length as tuple, push into a list as output
    l_crc.append((crc,l_size[id]))

print("crc16 :", l_crc, len(l_crc))


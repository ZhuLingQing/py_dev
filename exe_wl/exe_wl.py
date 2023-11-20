import sys,os,shutil
import subprocess
import shlex

from datetime import datetime
import time

_COLOR_DEFAULT_ = "\033[0m"
_COLOR_RED_ = "\033[31m"
_COLOR_GREEN_ = "\033[32m"
_COLOR_YELLOW_ = "\033[33m"
_COLOR_BLUE_ = "\033[1;34m"
_FAIL_ = _COLOR_RED_+"FAIL"+_COLOR_DEFAULT_
_PASS_ = _COLOR_GREEN_+"PASS"+_COLOR_DEFAULT_

# This is default path in tzhu environment
# You can use $GORDIAN_ROOT, $V8BINARY_ROOT, $MODELZOO_ROOT to override them.
dPath = {
    "GORDIAN"  : "/nfs/homes/tzhu/projects/pace2/gordian/",
    "V8BINARY" : "/nfs/homes/tzhu/projects/pace2/v8binary/",
    "MODELZOO" : "/nfs/homes/tzhu/projects/pace2/model_zoo.ssd18/"
}

dPathGOLDFINGER = "build_pld/_deps/gf_aurora-src"

dWorkloads = {
    "is64" : {
        "name": "ising64x64",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,12800,12800",
        "hex" : "ising/64x64/golden/ising64_input_wgt_regression.hex",
        "pe" : "build_pld/ising/64x64/nonai_ising64.elf",
        "output" : "ising/64x64/ising64_out_vec.hex.bin"
    },
    "is128" : {
        "name": "ising128x128",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,25600,25600",
        "hex" : "ising/128x128/golden/ising128_input_wgt_regression.hex",
        "pe" : "build_pld/ising/128x128/nonai_ising128.elf",
        "output" : "ising/128x128/ising128_out_vec.hex.bin"
    },
    "ln" : {
        "name": "linear-solver",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,128,128",
        "hex" : "linear-solver/golden/ln_input_wgt_regression.hex",
        "pe" : "build_pld/linear-solver/nonai_ln.elf",
        "output" : "linear-solver/ln_out.hex.bin"
    },
    "sc" : {
        "name": "spectral-clustering",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,128,128",
        "hex" : "spectral-clustering/golden/sc_input_wgt_regression.hex",
        "pe" : "build_pld/spectral-clustering/nonai_sc.elf",
        "output" : "spectral-clustering/sc_dv_out.hex.bin"
    },
    "mc" : {
        "name": "monte-carlo",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,128,4",
        "hex" : "monte-carlo/golden/mc_input_wgt_regression.hex",
        "pe" : "build_pld/monte-carlo/nonai_mlp.elf",
        "output" : "monte-carlo/mc_output.hex.bin"
    },
    "ssd18" : {
        "name": "ssd-resnet18",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,904000,904000",
        "hex" : "ssd_resnet18/golden/codegen_weight_input285_full_len.hex",
        "pe" : "build_pld/ssd_resnet18/ssd_res18.elf",
        "output" : "ssd-resnet18/output.hex.bin"
    },
    "ssd34" : {
        "name": "ssd-resnet34",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,1048576,904448",
        "hex" : "ssd_resnet34/golden/ssd34_input_wgt.hex",
        "pe" : "build_pld/ssd_resnet34/ssd_res34.elf",
        "output" : "ssd-resnet34/total_output_golden.bin",
        "post_proc" : "ssd34outputProc"
    },
    "res50" : {
        "name": "resnet50",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,1024,1000",
        "hex" : "resnet50/codegen_weight_e2e_lemur.hex",
        "pe" : "build_pld/resnet50/resnet50.elf",
        "output" : "resnet50/resnet50_56layers_output.hex.bin"
    },
    "res50bc2" : {
        "name": "resnet50bc2",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,2048,2048",
        "hex" : "resnet50_batch2_dc/golden/m3_mqbench_qmodel_deploy_no_pot_scale.hex",
        "pe" : "build_pld/resnet50_batch2_dc/resnet50bc2.elf",
        "output" : "resnet50/resnet50_56layers_batch2_output.hex.bin"
    }
}


def ssd34outputProc(file_path):
    l_gap = 32
    l_size = (563264, 51264, 204864, 12864, 51264, 3264, 12864,  832,   3200,   320,   384,   64)
    bary = readBinFile(file_path)
    baout = bytes()
    offset = 0
    for size in l_size:
        baout += bytes([0]*l_gap)
        baout += bary[offset + l_gap : offset + size]
        offset += size
    writeBinFile(file_path, baout)
    #return baout

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

def getSttyWidth():
    rows, columns = subprocess.check_output(['stty', 'size']).split()
    #print("%d rows, and %d cols" % (int(rows), int(columns)))
    return int(columns)

def getPath():
    # print repo commits
    kPath = [*dPath]
    print(_COLOR_BLUE_+"The commits of the repos:"+_COLOR_DEFAULT_)
    for kp in kPath:
        try:
            path_ = os.environ[kp+"_ROOT"]
            dPath[kp] = path_
        except:
            path_ = None
        if os.path.exists(dPath[kp]) == False:
            print(str.format("%-10s"%kp)+" : " + dPath[kp]+_COLOR_RED_+" Not exist "+_COLOR_DEFAULT_)
            sys.exit(1)
        print("%-10s : %s" % (kp, _COLOR_YELLOW_+getGitCommit(dPath[kp])+" ("+ getGitBranch(dPath[kp]) + ")" + _COLOR_DEFAULT_))
    print("%-10s : %s" % ("GF_AURORA", _COLOR_YELLOW_+getGitCommit(dPath[kp]+dPathGOLDFINGER)+" ("+ getGitBranch(dPath[kp]+dPathGOLDFINGER) + ")"+_COLOR_DEFAULT_))

def exeBash(cmd, timeout : int = None, disp : bool = False):
    tty_width = getSttyWidth() - 4
    start_t = datetime.now()
    max_len = 0
    llog = []
    cmd = shlex.split(cmd)
    rc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while rc.poll() == None:
        l = str(rc.stdout.readline(), encoding='utf-8')[0:-1]
        if len(l) > 0:
            llog.append(l)
            if disp == True: print(l[0:tty_width],end='\r')
            if len(l) > max_len: max_len = len(l)
    if disp == True and max_len:
        space_ = " "
        if max_len > tty_width: max_len = tty_width
        print(space_.center(max_len,' '),end='\r')
    rc.wait()
    return (rc.returncode, llog)

def md5sum(file_path_name):
    md5sum_cmd = "md5sum " + file_path_name
    rc = exeBash(md5sum_cmd)
    assert rc[0] == 0, "md5sum " + file_path_name + _FAIL_
    return rc[1][0].split(' ')[0]

def getGitCommit(path):
    os.chdir(path)
    cmd = shlex.split("git log -n 1")
    rc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rc.wait()
    l = str(rc.stdout.readline(), encoding='utf-8').split(' ')
    if l[0] != "commit":
        assert False, path + "can't get git commit"
    return l[1][0:-1]

def getGitBranch(path):
    commit = getGitCommit(path)
    cmd = shlex.split("git branch -r --contains " + commit)
    rc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rc.wait()
    l = str(rc.stdout.readline(), encoding='utf-8').split(' ')[-1]
    return l[0:-1]
    
def checkOutput(golden_file_path, output_path : str = '.'):
    md5_g = md5sum(golden_file_path)
    for i in range(0, 4):
        md5_o = md5sum(output_path + str.format("/output_%d.bin " % i))
        if md5_o != md5_g:
            print("MD5 check " + _FAIL_)
            return None
    return md5_g

def findFiles(path, name):
    filepath,fullflname = os.path.split(name)
    find_cmd = "find " + path + " -name " + fullflname
    rc = exeBash(find_cmd)
    #print("FIND: ",rc[1])
    return rc[1]

def checkFileExist(path_name):
    return os.path.exists(path_name)

def executeEndToEndTest(wl):
    # check whether all related files exist.
    if checkFileExist(dPath["MODELZOO"] + wl["hex"]) == False:
        print(str("%-20s" % wl["name"]), "input+weight hex file not exist")
        return 1
    if checkFileExist(dPath["MODELZOO"] + wl["pe"]) == False:
        print(str("%-20s" % wl["name"]), "firmware image elf file not exist")
        return 1
    if checkFileExist(dPath["V8BINARY"] + wl["output"]) == False:
        print(str("%-20s" % wl["name"]), "output binary file not exist")
        return 1
    # execute gordian script
    gordian_cmd = "./funcsim_lin " + wl["arg"] + " hex " + dPath["MODELZOO"] + wl["hex"] + " pe " + dPath["MODELZOO"] + wl["pe"] + " log f dump t dumpx " + wl["dumpx"]
    start_t = datetime.now()
    rc = exeBash(gordian_cmd, timeout = 5, disp = True)
    end_t = datetime.now()
    durn = (end_t - start_t).seconds
    if 0 != rc[0]:
        print(gordian_cmd)
        print("%-20s Gordian return %d %s" % (wl["name"], rc[0], _FAIL_))
        return rc[0]
    else:
        #if wl["name"] == "ssd-resnet34":
        if 'post_proc' in wl:
            for i in range(0, 4):
                eval(wl['post_proc'])(dPath["GORDIAN"]+str.format("output_%d.bin" % i))
        md5 = checkOutput(dPath["V8BINARY"] + wl["output"])
        if None == md5:
            print(str("%-20s" % wl["name"]), "MD5: not same!", _FAIL_)
            return 2
        else:
            print(str("%-20s" % wl["name"]), "MD5:", md5, _PASS_, str.format("take %ds" % durn))
    return 0

kWorkloads = [*dWorkloads]

if len(sys.argv) == 2:
    assert sys.argv[1] in kWorkloads, _COLOR_RED_+"arg1 not found in workload list: " + _COLOR_BLUE_+str(kWorkloads)+_COLOR_DEFAULT_
    kWorkloads = [sys.argv[1]]

#current_dir = os.path.dirname(os.path.abspath(__file__))
getPath()
# try find the elf files, if not exist try rebuild.
rc = findFiles(dPath["MODELZOO"], "*.elf")
if len(rc) == 0: #no elf found
    print(_COLOR_BLUE_+"No elf found, try to build."+_COLOR_DEFAULT_)
    os.chdir(dPath["MODELZOO"])
    rc = exeBash("make pld -j", disp = True)
    if rc[0] != 0:
        print("Build model_zoo %d %s." % (rc[0], _FAIL_))
        sys.exit(rc[0])
# jump to gordian folder, then run the gordian script
print(_COLOR_BLUE_+"The gordian end to end test:"+_COLOR_DEFAULT_)
os.chdir(dPath["GORDIAN"])
for kwl in kWorkloads:
    executeEndToEndTest(dWorkloads[kwl])
print(" >>>>> done <<<<<")
#os.chdir(current_dir)
sys.exit(0)
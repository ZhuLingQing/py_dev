import sys,os,shutil
import subprocess
import shlex

gordian_path = "/nfs/homes/tzhu/projects/pace2/gordian/"
v8binary_path = "/nfs/homes/tzhu/projects/pace2/v8binary/"
model_zoo_path = "/nfs/homes/tzhu/projects/pace2/model_zoo.ssd18/"

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
        "hex" : "ssd-resnet18/golden/codegen_weight_input285_full_len.hex",
        "pe" : "build_pld/ssd-resnet18/ssd_res18.elf",
        "output" : "ssd-resnet18/output.hex.bin"
    },
    "res50" : {
        "name": "resnet50",
        "arg" : "sel [mcp_4pe]",
        "dumpx" : "0x3000000,1024,1000",
        "hex" : "resnet50/codegen_weight_e2e_lemur.hex",
        "pe" : "build_pld/resnet50/resnet50.elf",
        "output" : "resnet50/resnet50_56layers_output.hex.bin"
    }
}

def reaadBinFile(file_path):
    try:
        binfile = open(file_path,'rb')
        size = os.path.getsize(file_path)
        data = binfile.read(size)
        #data = []
        #for i in range(size):
        #    data.append(binfile.read(1))
        binfile.close()
        return data
    except:
        assert False, "file not exist"

def exeBash(cmd, disp : bool = False):
    #print(cmd)
    #rec = os.system(cmd)
    #return rec
    cmd = shlex.split(cmd)
    rc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if disp == True:
        while rc.poll() == None:
            l = rc.stdout.readline()
            print(str(l, encoding='utf-8'))
    rc.wait()
    return rc.returncode

def md5sum(file_path_name):
    md5sum_cmd = "md5sum " + file_path_name
    #print(md5sum_cmd)
    cmd = shlex.split(md5sum_cmd)
    rc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rc.wait()
    if rc.returncode != 0:
        return None
    else:
        md5 = str(rc.stdout.readline(),encoding='utf-8')
        return md5.split(' ')[0]

def getGitCommit(path):
    os.chdir(path)
    cmd = shlex.split("git log -n 1")
    rc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rc.wait()
    l = str(rc.stdout.readline(), encoding='utf-8').split(' ')
    if l[0] != "commit":
        assert False, path + "can't get git commit"
    return l[1][0:-1]
    
def checkOutput(golden_file_path, output_path : str = '.'):
    md5_g = md5sum(golden_file_path)
    if None == md5_g:
        #print("md5sum(g)", golden_file_path, "FAIL")
        return None
    for i in range(0, 4):
        md5_o = md5sum(output_path + str.format("/output_%d.bin " % i))
        if None == md5_o:
            #print("md5sum(o)", output_path + str.format("/output_%d.bin " % i), "FAIL")
            return None
        #print("output:", md5_o)
        if md5_o != md5_g:
            #print(md5_g)
            #print(md5_o)
            #print("output %d isn't same" % i)
            return None
    return md5_g

kWorkloads = [*dWorkloads]

if len(sys.argv) == 2:
    assert sys.argv[1] in kWorkloads, "arg1 not found in workload list" + str(kWorkloads)
    kWorkloads = [sys.argv[1]]

current_dir = os.path.dirname(os.path.abspath(__file__))
print("Gordian : \033[33m" + getGitCommit(gordian_path)+"\033[0m")
print("ModelZoo: \033[33m" + getGitCommit(model_zoo_path)+"\033[0m")
print("v8binary: \033[33m" + getGitCommit(v8binary_path)+"\033[0m")
os.chdir(gordian_path)
for kwl in kWorkloads:
    wl = dWorkloads[kwl]
    gordian_cmd = "./funcsim_lin " + wl["arg"] + " hex " + model_zoo_path + wl["hex"] + " pe " + model_zoo_path + wl["pe"] + " log f dump t dumpx " + wl["dumpx"]
    rc = exeBash(gordian_cmd, disp = False)
    if 0 != rc:
        print(gordian_cmd)
        print("Gordian failed", str(rc))
        break
    md5 = checkOutput(v8binary_path + wl["output"])
    if None == md5:
        print(str("%-20s" % wl["name"]), "MD5: not same! \033[31mFAIL\033[0m")
        break
    else:
        print(str("%-20s" % wl["name"]), "MD5:", md5, "\033[32mPASS\033[0m")
print(" >>>>> done <<<<<")
os.chdir(current_dir)
sys.exit(rc)
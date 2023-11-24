import shutil,os,sys

_COLOR_DEFAULT_ = "\033[0m"
_COLOR_RED_ = "\033[31m"
_COLOR_GREEN_ = "\033[32m"
_COLOR_YELLOW_ = "\033[33m"
_COLOR_BLUE_ = "\033[1;34m"
_FAIL_ = _COLOR_RED_+"FAIL"+_COLOR_DEFAULT_
_PASS_ = _COLOR_GREEN_+"PASS"+_COLOR_DEFAULT_

dPath = {
    "V8BINARY" : "/nfs/homes/tzhu/projects/pace2/v8binary/",
    "MODELZOO" : "/nfs/homes/tzhu/projects/pace2/model_zoo.ssd18/"
}

# from, to
dWorkloads = {
    "is64" :  {"name" : "ising64", "modelzoo_sub_path" : "ising/64x64", "f_name" : "nonai_ising64" },
    "is128" : {"name" : "ising128", "modelzoo_sub_path" : "ising/128x128", "f_name" : "nonai_ising128" },
    "ln" : {"name" : "linear-solver", "modelzoo_sub_path" : "linear-solver", "f_name" : "nonai_ln" },
    "mlp" : {"name" : "monte-carlo", "modelzoo_sub_path" : "monte-carlo", "f_name" : "nonai_mlp" },
    "sc" : {"name" : "spectral-clustering", "modelzoo_sub_path" : "spectral-clustering", "f_name" : "nonai_sc" },
    "ssd18" : {"name" : "ssd_resnet18", "modelzoo_sub_path" : "ssd_resnet18", "v8binary_sub_path" : "ssd-resnet18", "f_name" : "ssd_res18" },
    "ssd34" : {"name" : "ssd_resnet34", "modelzoo_sub_path" : "ssd_resnet34", "v8binary_sub_path" : "ssd-resnet34", "f_name" : "ssd_res34" },
    "res50" : {"name" : "resnet50", "modelzoo_sub_path" : "resnet50", "f_name" : "resnet50" },
    "res50bc2" : {"name" : "resnet50_batch2", "modelzoo_sub_path" : "resnet50_batch2_dc", "v8binary_sub_path" : "resnet50_batch2", "f_name" : "resnet50bc2" },
}

cpy_file_ext = ("elf", "disasm", "bin")

repo_name = "model_zoo"
branch_name = "main"

#sign_script = dst_path + "tools/gf_aurora_sign/gf_aurora_sign"
sign_script = "python3 ./py_signature.py"

def __findArgValue(long_name : str, short_name : str = None):
    assert None == short_name or len(short_name) == 1, "invalid short_name"
    for i in range(1, len(sys.argv) - 1):
        arg = sys.argv[i]
        if arg[0:2] == '--' and arg[2:] == long_name: #long arg
            return sys.argv[i + 1]
        elif arg[0:1] == '-' and None != short_name and arg[1] == short_name[0]: #short arg
            return sys.argv[i + 1]
    return None

def __callBash(cmd, disp : bool = False):
    #print(cmd)
    rec = os.system(cmd)
    if str(rec).isdigit():
        return int(rec)
    if disp == True: print(rec)
    return -1

def CheckWorkload(wl):
    print(_COLOR_BLUE_+wl["name"]+":"+_COLOR_DEFAULT_)
    if "v8binary_sub_path" in wl:
        v8b_path = dst_path + wl["v8binary_sub_path"]
    else:
        v8b_path = dst_path + wl["modelzoo_sub_path"]
    sign_cmd = sign_script + " " + v8b_path + "/" + wl["f_name"] + "_sign.bin"
    if 0 != __callBash(sign_cmd):
        sys.exit(1)

def SignWorkload(wl, src_path, dst_path):
    print(_COLOR_BLUE_+wl["name"]+":"+_COLOR_DEFAULT_)
    if "v8binary_sub_path" in wl:
        v8b_path = dst_path + wl["v8binary_sub_path"]
    else:
        v8b_path = dst_path + wl["modelzoo_sub_path"]
    for ext in cpy_file_ext:
        cp_cmd = "cp " + src_path + wl["modelzoo_sub_path"] + "/" + wl["f_name"] + "." + ext + " " + v8b_path + "/"
        if 0 != __callBash(cp_cmd):
            sys.exit(1)
    sign_cmd = sign_script + " " + v8b_path + "/" + wl["f_name"] + ".bin " + " --branch " + branch_name + " --tag " + tag_name + " --repo " + repo_name + "  "
    if 0 != __callBash(sign_cmd):
        sys.exit(1)
    rm_cmd = "rm " + v8b_path + "/" + wl["f_name"] + ".bin" 
    if 0 != __callBash(rm_cmd):
        sys.exit(1)

def getPath(kPath):
    #print(_COLOR_BLUE_+"The commits of the repos:"+_COLOR_DEFAULT_)
    for kp in kPath:
        try:
            path_ = os.environ[kp+"_ROOT"]
            dPath[kp] = path_
        except:
            path_ = None
        if os.path.exists(dPath[kp]) == False:
            print(str.format("%-10s"%kp)+" : " + dPath[kp]+_COLOR_RED_+" Not exist "+_COLOR_DEFAULT_)
            sys.exit(1)
        #print("%-10s : %s" % (kp, _COLOR_YELLOW_+getGitCommit(dPath[kp])+_COLOR_DEFAULT_))

if __name__ == "__main__":
    tag_name = __findArgValue("tag")
    kWorkloads = [*dWorkloads]
    if tag_name != None:
        #cpy and signature
        getPath([*dPath])
        repo = __findArgValue("repo")
        if None != repo:
            repo_name = repo
        branch = __findArgValue("branch")
        if None != branch:
            branch_name = branch

        src_path = dPath["MODELZOO"]+"build_pld/"
        dst_path = dPath["V8BINARY"]
        if len(sys.argv) > 1 and sys.argv[1] in kWorkloads:
            SignWorkload(dWorkloads[sys.argv[1]], src_path, dst_path)
        else:
            for wl in kWorkloads:
                SignWorkload(dWorkloads[wl], src_path, dst_path)
    else:
        # check signature
        getPath(["V8BINARY"])
        dst_path = dPath["V8BINARY"]
        if len(sys.argv) > 1 and sys.argv[1] in kWorkloads:
            CheckWorkload(dWorkloads[sys.argv[1]])
        else:
            for wl in kWorkloads:
                CheckWorkload(dWorkloads[wl])
    
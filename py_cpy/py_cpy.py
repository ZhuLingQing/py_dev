import shutil,os,sys

src_path = "/nfs/homes/tzhu/projects/pace2/model_zoo.ssd18/build_pld/"
dst_path = "./"

# from, to
workloads = (
    {"name" : "ising64", "sub_path" : "ising/64x64", "f_name" : "nonai_ising64" },
    {"name" : "ising128", "sub_path" : "ising/128x128", "f_name" : "nonai_ising128" },
    {"name" : "ln", "sub_path" : "linear-solver", "f_name" : "nonai_ln" },
    {"name" : "mlp", "sub_path" : "monte-carlo", "f_name" : "nonai_mlp" },
    {"name" : "sc", "sub_path" : "spectral-clustering", "f_name" : "nonai_sc" },
    {"name" : "ssd-res18", "sub_path" : "ssd-resnet18", "f_name" : "ssd_res18" },
    #{"name" : "resnet50", "sub_path" : "resnet50", "f_name" : "resnet50bc1" },
    #{"name" : "resnet50_batch2_dc", "sub_path" : "resnet50_batch2", "f_name" : "resnet50" },
)

cpy_file_ext = ("elf", "disasm", "bin")

repo_name = "model_zoo"
branch_name = "main"

#sign_script = dst_path + "tools/gf_aurora_sign/gf_aurora_sign"
sign_script = "python3 ../py_signature/py_signature.py"

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
    print(cmd)
    rec = os.system(cmd)
    if str(rec).isdigit():
        return int(rec)
    if disp == True: print(rec)
    return -1

tag_name = __findArgValue("tag")
assert tag_name != None, "tag name is necessary"
repo = __findArgValue("repo")
if None != repo:
    repo_name = repo
branch = __findArgValue("branch")
if None != branch:
    branch_name = branch

for wl in workloads:
    for ext in cpy_file_ext:
        cp_cmd = "cp " + src_path + wl["sub_path"] + "/" + wl["f_name"] + "." + ext + " " + dst_path + wl["sub_path"] + "/"
        if 0 != __callBash(cp_cmd):
            sys.exit(1)
    sign_cmd = sign_script + " " + dst_path + wl["sub_path"] + "/" + wl["f_name"] + ".bin " + " --branch " + branch_name + " --tag " + tag_name + " --repo " + repo_name + "  "
    if 0 != __callBash(sign_cmd):
        sys.exit(1)
    rm_cmd = "rm " + dst_path + wl["sub_path"] + "/" + wl["f_name"] + ".bin" 
    if 0 != __callBash(rm_cmd):
        sys.exit(1)
    
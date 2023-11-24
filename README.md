# py_dev  

---
## py_bin_scaler  
- binary file data scaler.  
- cut off or insert zero from bitN to bitM.  
- which is used in model_zoo ising output resize.  
```bash
>python py_bin.py $bin_file_path_name $scale_from:$scale_to
```

---
## py_refresh
- curses library used in python.  
- no specific usage.  
```bash
>python py_refresh.py
```

---
## py_signature
- signature for binary image.  
- this script is dedicated for goldfinger/aurora tracking.   
```bash
# check the image file signature, and display the basic information  
>python py_signature.py $bin_file_path_name  
# sign the image file.  
>python py_signature.py $bin_file_path_name --repo $repo_name --tag $tag_name --branch $branch_name
```

---
## py_cpy
- use bash to copy file.  
- use bash to execute other script.   
- this script is dedicated for end to end test copy image to binary repo.   
```bash
>python py_cpy.py --tag $tag_name
```

---
## exe_wl.py
- use subprocess to execute bash and other script.  
- which could fetch process the output and return code.  
- support git commit fetch.  
- support os.chdir() path move.  
- this script is dedicated for gordian end to end verify.   
```bash
>python exe_wl.py
>python exe_wl.py $workload_name
```

---
## hex2bin.py
- convert model_zoo hex to binary.  
- support path and recursive.  

---
## py_utilities.py
### exe_bash.py
- execute bash command.  
- export:
    - exeBash() 
  
### file_rw.py
- binary file read and write.  
- export:
    - writeBinFile()
    - readBinFile()

### py_git.py
- git command.
- export:
    - git::
        - isRepo()
        - isClean()
        - getCommit()
        - getBranch()
        - getRepoUrl()
        - getRepoName()

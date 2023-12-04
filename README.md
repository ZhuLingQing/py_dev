# py_dev  

```bash
export PYTHONPATH=${pwd}$PYTHONPATH
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
## py_lgt_e2e

---
## py_utilities

### bin_compare.py
- compare two binary files.
- export:
    - bin_compare()  
```bash
>python bin_compare.py $bin_file1 $bin_file2 $break_on_diff $disp_per_line
```

## bin_scaler  
- binary file data scaler.  
- cut off or insert zero from bitN to bitM.  
- which is used in model_zoo ising output resize.  
```bash
>python bin_scaler.py $bin_file_path_name $scale_from:$scale_to
```

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
```bash
>python py_git.py $repo_path
```

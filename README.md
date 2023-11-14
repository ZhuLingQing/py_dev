# py_dev  

---
## py_bin  
-binary file data scaler.  
```bash
>python py_bin.py $bin_file_path_name $scale_from:$scale_to
```

---
## py_refresh
-curses library used in python.  
```bash
>python py_refresh.py
```

---
## py_signature
-signature for binary image.  
-this script is dedicated for goldfinger/aurora.   
```bash
# check the image file signature, and display the basic information  
>python py_signature.py $bin_file_path_name  
# sign the image file.  
>python py_signature.py $bin_file_path_name --repo $repo_name --tag $tag_name --branch $branch_name
```

---
## py_cpy
-use bash to copy file.  
-use bash to execute other script.   
-this script is dedicated for end to end test copy image to binary repo.   
```bash
>python py_cpy.py --tag $tag_name
```

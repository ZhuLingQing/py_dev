# py_lgt_e2e  
ligntelligence pace2 end to end test related scripts.  

## add_layout
resnet50 batch2:
- @gerald guess maybe the weight is in
- debugging replace "CHECK_WEIGHT()" with "CHECK_WEIGHT(layer)"  
- only use once
```bash
>python add_layout.py
```

## bc2_to_bc1.py
resnet50 batch2:  
- replace all operators' batch2 counter with a 'BATCH_COUNT' macro.  
```bash
>python bc2_to_bc1.py
```

### bin2hex.py
- convert model_zoo binary to hex.  
```bash
>python bin2hex.py $bin_file_path_name
```

## diff_layer
resnet50 batch2:  
- input an offset, it will return which middle-layer it located.
- get difference layer
```bash
>python diff_layer.py $difference_offset
```

## filtrate_layout.py
resnet50 batch2:
- compute a res50bc2 each layer's const's crc16.
- output a array to c code for the verification.
```bash
>python filtrate_layout.py
```

### hex2bin.py
- convert model_zoo hex to binary.  
- support path and recursive.  
```bash
>python hex2bin.py $hex_file_path_name
```

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

## zero_fill.py
resnet50 batch2:
- palladium output has 32B random prefix and postfix.
- replace them with 0x00.
```bash
>python zero_fill.py $output_path_name
```

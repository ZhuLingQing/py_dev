import sys,os,shutil
import subprocess
import shlex
import exe_bash as exe_bash

def remove_excess_space(sin : str):
    sout = str("")
    prevIsSpace = False
    for i in range(len(sin)):
        if sin[i]==' ':
            if prevIsSpace==False:
                sout += sin[i]
            prevIsSpace = True
        else:
            sout += sin[i]
            prevIsSpace = False
    return sout

if __name__ == "__main__":
    num_killed = 0
    if len(sys.argv) < 3:
        print("arg1: user_name")
        print("arg2: key_word")
        sys.exit(1)
    usr_name = sys.argv[1]
    key_word = sys.argv[2]
    rc = exe_bash.exeBash("ps -au")
    if rc[0] != 0:
        print("return %d" % rc[0])
    else:
        for l in rc[1]:
            s = remove_excess_space(l).split(' ')
            if s[0] == usr_name and s[10].find(key_word) != -1:
                print("Found thread:", s[1])
                exe_bash.exeBash("kill -9 "+ s[1])
                num_killed += 1
    if num_killed > 0:
        print("Killed %d" % num_killed)
    else:
        print("No thread found.")
    sys.exit(1)

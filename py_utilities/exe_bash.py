import sys,os,shutil
import subprocess
import shlex

# get terminal window width, return int columns
def getSttyWidth():
    rows, columns = subprocess.check_output(['stty', 'size']).split()
    #print("%d rows, and %d cols" % (int(rows), int(columns)))
    return int(columns)

# execute bash command
# cmd     : command string
# timeout : timeout seconds.
# display : print or not.
# return  : tuple[2] : [0] = return code, [1] = list of trace log
def exeBash(cmd : str, timeout : int = None, display : bool = False):
    tty_width = getSttyWidth() - 4
    llog = []
    cmd = shlex.split(cmd)
    rc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while rc.poll() == None:
        l = str(rc.stdout.readline(), encoding='utf-8')[0:-1]
        if len(l) > 0:
            llog.append(l)
            if display == True: print(l[0:tty_width]+' '*(tty_width - len(l[:tty_width])), end='\r')
    if display is True:
        print(' '*tty_width, end='\r')
    rc.wait()
    while True:
        l = str(rc.stdout.readline(), encoding='utf-8')
        if l is None or len(l) == 0: break
        llog.append(l[:-1])
    return (rc.returncode, llog)

if __name__ == "__main__":
    rc = exeBash(sys.argv[1], display=True)
    if rc[0] != 0:
        print("return error:", rc[0])
    else:
        print(rc[1])
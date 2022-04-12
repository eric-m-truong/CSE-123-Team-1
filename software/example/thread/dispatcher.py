from os import wait
import subprocess
import shlex
import shutil

tuplize = lambda x: (subprocess.Popen(x, shell=True).pid, x)
acquire_new_pid = lambda x: tuplize(x[1])

ps = [tuplize("python3 echo_loop.py"),
      tuplize("python3 echo_loop.py")]

while (True):
    pid, ret = wait()
    for i in range(len(ps)):
        p = ps[i]
        if p[0] == pid:
            ps[i] = acquire_new_pid(p)
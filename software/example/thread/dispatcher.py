from multiprocessing import Semaphore
import signal, sys
from os import wait
import subprocess
import shlex
import shutil
import time

from numpy import true_divide
# from subprocess import run, Popen, PIPE

child_echo = lambda x: (subprocess.Popen(x, shell=True).pid, x)
acquire_new_pid = lambda x: child_echo(x[1])

# (pid, cmd)

# fork 2 echo proccesses and save their pids
ps = [child_echo("python3 echo_loop.py"), child_echo("python3 echo_loop.py")]

print(ps)

# for(ever)
#   pid = wait(NULL)
#   figure out which process had that pid
#   restart the process
#   save the new pid

while (True):
    pid, ret = wait()
    for i in range(len(ps)):
        p = ps[i]
        if p[0] == pid:
            ps[i] = acquire_new_pid(p)
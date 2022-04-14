from os import wait
import subprocess
import shlex
import shutil
from collections import namedtuple

Process = namedtuple("Process", ['pid', 'cmd'])
tuplize = lambda x: Process(subprocess.Popen(x, shell=True).pid, x)
acquire_new_pid = lambda x: tuplize(x.cmd)

ss = ["python3 echo_loop.py",
      "python3 echo_loop.py"]
ps = [tuplize(s) for s in ss] #  evaluating this line starts processes

while (status := wait()) != -1:
  pid, ret = status
  for i, p in enumerate(ps):
    if p.pid == pid:
      print("restarted", p.pid, end=" ")
      ps[i] = acquire_new_pid(p)
      print("as", ps[i].pid)

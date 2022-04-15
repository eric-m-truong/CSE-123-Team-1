from os import wait, fork, getpid, execv
import subprocess
from time import sleep
from sys import exit
from shutil import which

def spawn_child():
  if (pid := fork()) == 0:
    execv(which("python"), ["python", "echo_loop.py"])

for i in range(5):
  spawn_child()

try:
  while True:
    chid, ret = wait()
    print("reaped", chid)
    spawn_child()
except ChildProcessError:
  pass

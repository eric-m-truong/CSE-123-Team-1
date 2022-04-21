from os import wait, fork, getpid, execvpe
from sys import exit
from shutil import which
from pathlib import Path
from datetime import datetime, timedelta
import logging


BURST_MAX = 5

def execfn(fn, *args, **kwargs):
  pid = fork()
  if pid == 0:
    fn(*args, **kwargs)
  return pid


def exec(proc, args=None, /, *, env=None):
  fn = lambda: execvpe(which(proc), [proc, *args], env)
  return execfn(fn)


class Process:
  def __init__(self, exec):
    self.exec = exec
    self.pid = self.exec()
    self.burst = (-1, 0)

  def acquire_new_pid(self):
    self.pid = self.exec()


def run(es):
  # TODO: delay between creation... or you know we can just redispatch
  ps = [Process(e) for e in es]

  try:
    while True:
      chid, ret = wait()
      for p in ps:
        if p.pid == chid:
          logging.debug(f"reaped {chid}")
          if p.burst[1] == BURST_MAX:
            logging.critical(f"not restarting {chid}: burst limit exceeded")
            continue # don't restart
          p.acquire_new_pid()
          # burst limit: if a process restarts enough times in given threshold,
          # don't restart
          min = datetime.now().minute
          p.burst = (min, p.burst[1]+1) if p.burst[0] == min else (min, 0)
  except ChildProcessError:
    pass


if __name__ == '__main__':
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  es = [(exec, ('sleep', ['1'])), (exec, ('sleep', ['2']))]
  run(es)

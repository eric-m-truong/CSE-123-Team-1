from os import wait, fork, getpid, execvpe
from sys import exit
from shutil import which
from pathlib import Path
import logging


def execfn(fn, args=()):
  pid = fork()
  if pid == 0:
    fn(*args)
  return pid


def exec(proc, args=None, /, *, env=None):
  fn = lambda: execvpe(which(proc), [proc, *args], env)
  return execfn(fn)


class Process:
  def __init__(self, exec):
    self.exec = exec
    self.pid = self.exec()

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
          p.acquire_new_pid()
  except ChildProcessError:
    pass


if __name__ == '__main__':
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  es = [(exec, ('sleep', ['1'])), (exec, ('sleep', ['2']))]
  run(es)

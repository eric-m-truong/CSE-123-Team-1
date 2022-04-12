import subprocess
import shlex
import shutil

from numpy import true_divide
# from subprocess import run, Popen, PIPE

child_echo = lambda x: subprocess.run(f'while true; do echo {x}; done')
def child_echo2(x):
    command_line = shlex.split(f'{x}')
    command_line.insert(0, shutil.which('echo'))
    # print(command_line)
    return subprocess.Popen(command_line)


# Pid storage
class Process_ids:
    __slots__ = ['p1', 'p2']

# fork 2 echo proccesses and save their pids
saved_pids = Process_ids()
saved_pids.p1 = child_echo2("echoing 1!").pid
saved_pids.p2 = child_echo2("echoing 2!").pid
print(f'pid1: {saved_pids.p1}')
print(f'pid2: {saved_pids.p2}')

# for(ever)
#   pid = wait(NULL)
#   figure out which process had that pid
#   restart the process
#   save the new pid

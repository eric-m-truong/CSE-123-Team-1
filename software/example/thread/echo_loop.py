import time
import os
from random import random

# print(os.getpid(), i)
for i in range(2):
  print(os.getpid(), i)
  # time.sleep(random())
  time.sleep(1)

print(os.getpid(), "exit")

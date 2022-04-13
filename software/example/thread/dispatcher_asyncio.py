import asyncio
import time


async def echo(i):
  """ Print j i times, then throw an error. """
  for j in range(2):
    print(i, j)
    await asyncio.sleep(i + 1) # yields to other coroutines
  raise Exception # simulate failure


async def forever(f, *args):
  """ Keeps running a coroutine forever, even in the event of an exception. """
  while True:
    try:
      await f(*args)
    except Exception:
      pass
    print(f'{f}: restarting')


async def main():
  """ Schedule infinitely running tasks and await their return (which never
      occurs) """
  tasks = [forever(echo, i) for i in range(5)]
  await asyncio.gather(*tasks)


asyncio.run(main())

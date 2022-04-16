- reads config once by using fact that module loading is cached
- assigns contents of config to module namespace

`config.py` prints a message whenever it is loaded.

observe that when `a.py` is ran, it imports `config.py` and `b.py`, and `b.py`
in turn imports `config.py`, however we only see the message indicating
`config.py` was loaded once.

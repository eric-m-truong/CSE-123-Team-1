# installation

run `script/venv` (you _could_ also run script/run, it will run this if needed)

# running

run `script/run [args]` where args are flags that will be passed onto main.py.
passing `--help` will list flags.

## notes about oracle server

python3.10 on ubuntu is messy. See [1]

```
add-apt-repository ppa:deadsnakes/ppa
add-apt update
apt-get install python3.10{,-venv,-distutils}
```

at this point, the `python3.10` may run without the virtual environment.

[1]: https://stackoverflow.com/a/59334690

# each directory should have a readme that contains

- usage
- purpose
- todo / plans

# main server, modules

all python scripts that depend on libs in this dir must be run from this dir

main should create threads:
- [x] flask server by calling a (yet undefined) `run` function `server.handler`
- [x] an mqtt client to listen for data from the plugs

the server needs to:
- [ ] efficiently store data from the mqtt messages
- [x] send ctrl sigs to plugs after a user visits / posts to a url that sends a
  control signal
- [ ] be easily deployable

it would be nice if the server also:
- server periodically optimizes / does some calculations e.g. when asking for a
  sum (left vague intentionally)
- reports state of the plugs accurately
- had security

# explanations of directories

dir | purpose
----|--------
example|complete proof of concet files that can be used to make other things
client|mockups that illustrate what a complete user-facing page might look like
server|flask webserver module that serves html pages
db|module for interacting with db file
script|utility files that can generate plug data or aid in testing
plot|module that contains various bokeh plots to be used in html webpages
mqtt|scripts intended primarily to interact with and maintain an mqtt connection

future: test dir for testing aspects of server?

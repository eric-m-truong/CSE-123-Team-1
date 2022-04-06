# each directory should have a readme that contains

- usage
- purpose
- todo / plans

# main server, modules

all python scripts that depend on libs in this dir must be run from this dir

main should create threads:
- flask server by calling a (yet undefined) `run` function `server.handler`
- an mqtt client to listen for data from the plugs

the server needs to:
- efficiently store data from the mqtt messages
- send ctrl sigs to plugs after a user visits / posts to a url that sends a
  control signal
- be easily deployable

it would be nice if the server also:
- server periodically optimizes / does some calculations e.g. when asking for a
  sum (left vague intentionally)
- reports state of the plugs accurately
- had security

# explanations of directories

dir | purpose
----|--------
example|complete proof of concet files that can be used to make other things
mockup|mockups that illustrate what a complete user-facing page might look like
server|flask webserver module that serves html pages
db|module for interacting with db file
script|utility files that can generate plug data or aid in testing
plot|module that contains various bokeh plots to be used in html webpages

future: test dir for testing aspects of server?

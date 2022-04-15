for w/e reason, subprocess method will occassionally not read queued pid if
multiple
processes end @ the same time

this seems not to occur with manual fork, but logic is much harder to follow

asyncio ends up being pretty elegant. if what we need the server to run in
threads play nicely when run concurrently (NOT separate threads) then this would
be a good solution.

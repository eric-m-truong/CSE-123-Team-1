# Data

## Reasoning:

`DB_PATH` is the absolute path of the sqlite3 database, based on the directory
the script iis run from. This should avoid any relative path messiness.

```
[cwd]/data/data.sqlite
```

# datagen

create a database file "data.sqlite", populate Plugs table with `PLUG_NUM` plugs
and a random MAC, then populate Data table with random data using the MAC of any
of the plugs and a power reading in range (0,1)

# Docs

See files themselves for docs on specific functions

Module | Purpose
-----|--------
query|string constants used in execute()
connection|connecting to and executing db commands
util|common db fns
table_classes|helper structs used with `add_plug` and `add_data`
datagen|create db data 24h before current date

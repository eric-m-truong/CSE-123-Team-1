# Data

## Reasoning:

`DB_PATH` is the absolute path of the sqlite3 database, based on the directory
the script iis run from. This should avoid any relative path messiness.

```
[cwd]/data/data.sqlite
```

# Docs

See files themselves for docs on specific functions

Module | Purpose
-----|--------
query|string constants used in execute()
connection|connecting to and executing db commands
util|common db fns
table_classes|helper structs used with `add_plug` and `add_data`

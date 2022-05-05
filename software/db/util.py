from dataclasses import asdict

from db import table_classes, query
from db.connection import execute, executemany


add_plug = lambda con, plug: execute(con, query.INS_PLUG, asdict(plug))
add_data = lambda con, dp: execute(con, query.INS_DATA, asdict(dp))
add_data_many = lambda con, ds: \
    executemany(con, query.INS_DATA, map(asdict, ds))
# can only ever return one row or nothing
get_plug_by_mac = lambda con, mac: \
  execute(con, query.SEL_PLUG_BY_MAC, mac).fetchone()
get_sum = lambda con: execute(con, query.SEL_PLUG_SUM)
get_range = lambda con, rng: execute(con, query.SEL_DATA_RANGE, rng)
get_uniq_ts = lambda con, rng: execute(con, query.SEL_UNIQ_TS, rng)
upd_alias = lambda con, alias, plug: execute(con, query.UPD_ALIAS, alias, plug)
get_by_approx_ts = lambda con, ts: execute(con, query.SEL_DATA_BY_APPROX_TS, ts)
get_24h_avg_by_hr = lambda con: execute(con, query.SEL_PLUG_DAY_AVG_BY_HR)
upd_status = lambda con, on, plug: execute(con, query.UPD_STATUS, on, plug)

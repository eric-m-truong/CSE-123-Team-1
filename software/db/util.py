from dataclasses import asdict

from db import table_classes, query
from db.connection import execute


add_plug = lambda con, plug: execute(con, query.INS_PLUG, asdict(plug))
add_data = lambda con, dp: execute(con, query.INS_DATA, asdict(dp))
# can only ever return one row or nothing
get_plug_by_mac = lambda con, mac: \
  execute(con, query.SEL_PLUG_BY_MAC, mac).fetchone()
get_sum = lambda con: execute(con, query.SEL_PLUG_SUM)
get_24h = lambda con: execute(con, query.SEL_DATA_24H)
get_uniq_ts = lambda con, range: execute(con, query.SEL_UNIQ_TS(range))
upd_alias = lambda con, alias, plug: execute(con, query.UPD_ALIAS, alias, plug)

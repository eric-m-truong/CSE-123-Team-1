from dataclasses import asdict

from db import table_classes, query
from db.connection import execute


add_plug = lambda con, plug: execute(con, query.INS_PLUG, asdict(plug))
add_data = lambda con, dp: execute(con, query.INS_DATA, asdict(dp))
get_plug_by_mac = lambda con, mac: execute(con, query.SEL_PLUG_BY_MAC, mac)
get_sum = lambda con: execute(con, query.SEL_PLUG_SUM)

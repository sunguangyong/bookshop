

import pyconf.db.realtime_db as realtime_db
import pyconf.db.realtime_hangzhou as realtime_hangzhou


config_A = realtime_hangzhou.config
config_B = realtime_db.config

ignores = [
    "tj_dic_center_address",
    "temp",
    "table_oneself",
    "gszd_city_code",
    "gszd_sync_adapter",
]

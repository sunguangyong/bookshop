

import pyutil.db.mellow as mellow
import pyutil.db.db_config_example as config


mellow = mellow.mellow(config.config)


def main():
    rows = mellow.Find("user", [], out=dict)
    print rows

    mellow.Insert("user", {"name":"liuzhuohua", "age":12, "weight":123.2})
    mellow.Insert("user", {"name":"zhuohua", "age":12, "weight":123.2})

    mellow.Delete("user", {"name": "zhuohua"})

    print mellow.Find("user", [], "name='liuzhuohua'", out=dict)

    print mellow.FieldInt("user", "id", "name='must'", default=-1)


if __name__ == '__main__':
    main()



import pyutil.db.mellow as mellow


if __name__ == '__main__':
    import pyutil.db.db_config_example as db_config_example
    mellow = mellow.mellow(db_config_example.config)
    print mellow.Update("user", {"name": "1111"}, {"id":4})
    print mellow.Find("user", ["`id`","name as uame"], limit=(2,2), out=dict)

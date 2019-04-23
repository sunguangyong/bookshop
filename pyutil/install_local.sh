#!/ bin/bash
#sh ./pydeps.sh

set -x

env=$1

HOMEPATH=`pwd`

echo $HOMEPATH

if [[ $env == "" ]]; then
    echo "Usage:\n    sh ./install.sh [ol test dev]"
    exit
fi


rm -f $HOMEPATH/db/config/manna.py
ln -s $HOMEPATH/db/config/manna_$env.py $HOMEPATH/db/config/manna.py

rm -f $HOMEPATH/db/config/manna_maint.py
ln -s $HOMEPATH/db/config/manna_maint_$env.py $HOMEPATH/db/config/manna_maint.py

rm -f $HOMEPATH/db/config/manna_statistic.py
ln -s $HOMEPATH/db/config/manna_statistic_$env.py $HOMEPATH/db/config/manna_statistic.py

rm -f $HOMEPATH/db/config/manna_patrol.py
ln -s $HOMEPATH/db/config/manna_patrol_$env.py $HOMEPATH/db/config/manna_patrol.py

rm -f $HOMEPATH/db/config/manna_apps.py
ln -s $HOMEPATH/db/config/manna_apps_$env.py $HOMEPATH/db/config/manna_apps.py

rm -f $HOMEPATH/api_proxy_jupiter/config/host_config.py
ln -s $HOMEPATH/api_proxy_jupiter/config/host_config_$env.py $HOMEPATH/api_proxy_jupiter/config/host_config.py

rm -f $HOMEPATH/db/config/manna_history.py
ln -s $HOMEPATH/db/config/manna_history_$env.py $HOMEPATH/db/config/manna_history.py


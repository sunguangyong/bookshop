
#sh ./pydeps.sh


env=$1

if [[ $env == "" ]]; then
    echo "Usage:\n    sh ./install.sh [ol test dev]"
    exit
fi


rm -f /opt/fubang/pyutil/db/config/manna.py
ln -s /opt/fubang/pyutil/db/config/manna_$env.py /opt/fubang/pyutil/db/config/manna.py

rm -f /opt/fubang/pyutil/db/config/manna_maint.py
ln -s /opt/fubang/pyutil/db/config/manna_maint_$env.py /opt/fubang/pyutil/db/config/manna_maint.py

rm -f /opt/fubang/pyutil/db/config/manna_statistic.py
ln -s /opt/fubang/pyutil/db/config/manna_statistic_$env.py /opt/fubang/pyutil/db/config/manna_statistic.py

rm -f /opt/fubang/pyutil/db/config/manna_patrol.py
ln -s /opt/fubang/pyutil/db/config/manna_patrol_$env.py /opt/fubang/pyutil/db/config/manna_patrol.py

rm -f /opt/fubang/pyutil/db/config/manna_apps.py
ln -s /opt/fubang/pyutil/db/config/manna_apps_$env.py /opt/fubang/pyutil/db/config/manna_apps.py

rm -f /opt/fubang/api_proxy_jupiter/config/host_config.py
ln -s /opt/fubang/api_proxy_jupiter/config/host_config_$env.py /opt/fubang/api_proxy_jupiter/config/host_config.py

rm -f /opt/fubang/pyutil/db/config/manna_history.py
ln -s /opt/fubang/pyutil/db/config/manna_history_$env.py /opt/fubang/pyutil/db/config/manna_history.py


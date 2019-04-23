

cd /opt/fubang/pyutil && git pull && cd ..
cd /opt/fubang/storage_api && git pull && cd ..
cd /opt/fubang/common_api && git pull && cd ..
cd /opt/fubang/api_proxy_jupiter && git pull && cd ..
cd /opt/fubang/app_proxy_jupiter && git pull && cd ..

systemctl restart storage-api.service
systemctl restart api-proxy-jupiter.service
systemctl restart app-proxy-jupiter.service


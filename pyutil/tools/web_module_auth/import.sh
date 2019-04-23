#!/bin/bash


rm -rf ./pyutil/tools/web_module_auth/auth_*

cp ./pyutil/tools/web_module_auth/data/1010109.json ./pyutil/tools/web_module_auth/auth_1.json
cp ./pyutil/tools/web_module_auth/data/2010201.json ./pyutil/tools/web_module_auth/auth_2.json
cp ./pyutil/tools/web_module_auth/data/4010432.json ./pyutil/tools/web_module_auth/auth_4.json
cp ./pyutil/tools/web_module_auth/data/6010614.json ./pyutil/tools/web_module_auth/auth_6.json


python -m pyutil/tools/web_module_auth/upload_template_module 1010108 
python -m pyutil/tools/web_module_auth/upload_template_module 1010109 
python -m pyutil/tools/web_module_auth/upload_template_module 1010110 
python -m pyutil/tools/web_module_auth/upload_template_module 2010201
python -m pyutil/tools/web_module_auth/upload_template_module 2010202
python -m pyutil/tools/web_module_auth/upload_template_module 2010203
python -m pyutil/tools/web_module_auth/upload_template_module 4010430
python -m pyutil/tools/web_module_auth/upload_template_module 4010432
python -m pyutil/tools/web_module_auth/upload_template_module 6010612
python -m pyutil/tools/web_module_auth/upload_template_module 6010613
python -m pyutil/tools/web_module_auth/upload_template_module 6010614
python -m pyutil/tools/web_module_auth/upload_template_module 6010615

python -m pyutil/tools/web_module_auth/upload_module 1
python -m pyutil/tools/web_module_auth/upload_module 2
python -m pyutil/tools/web_module_auth/upload_module 4
python -m pyutil/tools/web_module_auth/upload_module 6




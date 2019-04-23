#!/usr/local/bin/python
# -*- coding: utf8 -*- 

import sys
from flask import Flask
from flask_restful import Api, Resource

% for item in tables:
from dotage.${item["dbname"]}_api.${item["name"]} import ${item["who"]}ListApi, ${item["who"]}Api
%endfor



if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    app = Flask(__name__)
    api = Api(app)
    
% for item in tables:
    api.add_resource(${item["who"]}ListApi, '/${item["dbname"]}/${item["name"]}s', endpoint = '${item["name"]}s')
    api.add_resource(${item["who"]}Api, '/${item["dbname"]}/${item["name"]}/<int:id>', endpoint = '${item["name"]}')
%endfor

    app.run(host='0.0.0.0', port=9393, debug=False)

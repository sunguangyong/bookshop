#!/usr/local/bin/python
# -*- coding: utf8 -*- 

from flask import request
from flask_restful import Resource, reqparse
import json
import math
from pyutil.db.mellow import mellow

from dotage.fire_investigation_dbconfig import config as dbconfig

mellow = mellow(dbconfig)
parser = reqparse.RequestParser()
parser.add_argument('data', type=str)
${WHO}_TABLE_NAME = '${table_name}'

class ${WHO}ListApi(Resource):
    def get(self):
        result = {}
        count = int(query_dict.get("size", 20))
        start = int(query_dict.get("page", 0)*count)
        fields = ${table_name}.get("filter")
        query_dict = dict(filter(lambda x: x[0] in fields, request.args.items()))
        result['data'] = mellow.Find( ${WHO}_TABLE_NAME, [], query_dict, limit=(start,count), out=dict ) 
        result['total'] = mellow.Count( ${WHO}_TABLE_NAME, query_dict )
        result['code'] = 1
        result['msg'] = ''
        return result, 201

    def post(self):
        result = {}
        count, id = mellow.Insert(${WHO}_TABLE_NAME, data)
        result['data'] = mellow.Find( ${WHO}_TABLE_NAME, [], {'id':id} ) 
        result['code'] = 1
        result['msg'] = ''
        return result, 201

class ${WHO}Api(Resource):
    def get(self, id):
        result = {}
        result['data'] = mellow.Find( ${WHO}_TABLE_NAME, [], {"id": id}, out=dict ) 
        result['code'] = 1
        result['msg'] = ''
        return result, 201

    def put(self, id):
        result = {}
        data = json.loads(req_data)
        result['data'] = mellow.Update( ${WHO}_TABLE_NAME, data, {'id':id} ) 
        result['code'] = 1
        result['msg'] = ''
        return result, 201

    def delete(self, id): 
        result = {}
        mellow.Delete( ${WHO}_TABLE_NAME, {'id': id} )
        result['data'] = {}
        result['code'] = 1
        result['msg'] = ''
        return result, 201

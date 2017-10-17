#!/usr/bin/env python
# coding: utf-8
# @File Name: tspredict.py
# @Author: Joshua Liu
# @Email: liuchaozhenyu@gmail.com
# @Create Date: 2017-10-16 16:10:57
# @Last Modified: 2017-10-17 17:10:28
# @Description:
#   flask 框架实现的 Restful API 接口

from flask import Flask
from flask_restful import Resource
from flask_restful import Api
from flask_restful import reqparse
from flask_restful.reqparse import Argument
from flask_restful import abort
from werkzeug.datastructures import FileStorage
from io import StringIO
import uuid
import csv
import sys
import os

app = Flask(__name__)
api = Api(app)

ddir = './data/'
if not os.path.isdir(ddir):
    os.mkdir(ddir)

class Root(Resource):
    '''
    根，目前返回使用说明
    '''
    def get(self):
        return 'api 说明：\n/data/: 上传数据\narima/<id> 请求 arima 算法'


api.add_resource(Root, '/')


class FileStorageArgument(Argument):
    '''
    用于 flask-restful 接受所有的上传文件
    '''
    def convert(self, value, op):
        if self.type is FileStorage:
            return value
        super(FileStorageArgument, self).convert(**args, **kwargs)

#
# DataApi
#
data_dict = {}
for fl in os.listdir(ddir):
    if fl.endswith('.csv'):
        data_dict[fl[:-4]] = ddir + fl

class DataApi(Resource):
    '''
    数据接口
    '''
    def __init__(self):
        self.parser = reqparse.RequestParser(argument_class=FileStorageArgument)
        self.parser.add_argument('file', required=True, type=FileStorage, help='csv file', location='files')
        super(DataApi, self).__init__()

    def put(self):
        args = self.parser.parse_args()
        csvfile = args['file']

        # TODO: 文件检查

        fio = StringIO()
        csvfile.save(fio)
        return fio


    def post(self):
        args = self.parser.parse_args()
        csvfile = args['file']
        fid = self.genid()
        with open(ddir + fid + '.csv', 'wb') as f:
            csvfile.save(f)
        data_dict[fid] = ddir + fid + '.csv'
        return {'id': fid}

    def genid(self):
        newid = str(uuid.uuid4())[:8]
        ids = data_dict.keys()
        while newid in ids:
            newid = str(uuid.uuid4())[:8]
        return newid


api.add_resource(DataApi, '/data/')


from algorithm.arima import ArimaModel

class ArimaApi(Resource):
    '''
    '''
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('api', required=True, type=str)
        super(ArimaApi, self).__init__()


    def get(self, fid):
        self.abort_if_id_not_exist(fid)
        args = self.parser.parse_args()
        api = args['api']
        arima = ArimaModel(data_dict[fid])
        return {api: arima.callback(api).tolist()}

    def post(self):
        pass

    def put(self):
        pass


    def abort_if_id_not_exist(self, fid):
        if fid not in data_dict.keys():
            abort(404, message="{} is not exist".format(fid))

api.add_resource(ArimaApi, '/arima/<string:fid>')

if __name__ == '__main__':
    app.run(debug=True)

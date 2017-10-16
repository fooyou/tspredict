#!/usr/bin/env python
# coding: utf-8
# @File Name: tspredict.py
# @Author: Joshua Liu
# @Email: liuchaozhenyu@gmail.com
# @Create Date: 2017-10-16 16:10:57
# @Last Modified: 2017-10-16 17:10:55
# @Description:
#   flask 框架实现的 Restful API 接口

from flask import Flask
from flask.ext.restful import Resource
from flask.ext.restful import Api
from flask.ext.restful import reqparse
from flask.ext.restful import abort

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('data', type=str)

class Root(Resource):
    '''
    根，目前返回使用说明
    '''
    def get(self):
        return {'tspredict': 'OK'}


api.add_resource(Root, '/')


class Prediction(Resource):
    '''
    第三方接口封装
    '''
    def get(self):
        return {'prediction': 'foo'}

    def post(self):
        args = parser.parse_args()
        data = args['data']
        return data

    def put(self):
        pass

api.add_resource(Prediction, '/api/')

if __name__ == '__main__':
    app.run(debug=True)

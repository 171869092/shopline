#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,abort
import flask
import os
import pandas as pd

app = Flask(__name__)
from shopifyLive.shopifyOper import *
@app.route('/')
def test():
    return shopApi()

@app.route('/uoload',methods=['post'])
def upload():
    if request.method == 'POST':
        try:
            files = request.files['action']
            if not files:
                return internal_server_error(500)
            data = pd.read_csv(files)
            datas = pd.DataFrame(data)
            for x in range(len(datas)):
                row = datas[x:x + 1]
                order_id = row['order_id'][x]
                tracking_number = row['tracking_number'][x]
                dictData = {'order_id': order_id, 'tracking_number': tracking_number}
                shopifyOper().uploadTracking(dictData)
        except Exception as e:
            raise e
            # return internal_server_error(500)
    return '上传成功'

@app.errorhandler(400)
def internal_server_error(e):
    return '系统错误'

def shopApi():
    s = shopifyOper()
    s.pullOrder()
    return '成功'

if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    app.run()
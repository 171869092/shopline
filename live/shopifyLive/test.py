#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,abort
import flask
import os
import sys
import pandas as pd
import xlrd
sys.path.append('/home/shopify/shopifyLive')
app = Flask(__name__)
from shopifyOper import *
@app.route('/')
def test():
    return shopApi()


#. 上传页面
@app.route('/upload-file')
def form():
    return """
        <html>
            <body>
                <h1>Transform a file demo</h1>

                <form action="/transform" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """



#. 处理上传文件
@app.route('/transform',methods=['post','get'])
def transform():
    if request.method == 'POST':
        file = request.files['data_file']
        if not file:
            return internal_server_error(500)
        check = check_file_type(file.filename)
        if check == 'csv':
            data = pd.read_csv(file)
            datas = pd.DataFrame(data)
            for x in range(len(datas)):
                row = datas[x:x + 1]
                order_id = row['order_id'][x]
                tracking_number = row['tracking_number'][x]
                store = row['store_id'][x]
                dictData = {'order_id': order_id, 'tracking_number': tracking_number, 'store': store}
                shopifyOper().uploadTracking(dictData)
        elif check in ['xls', 'xlsx']:
            data = pd.read_excel(file)
            resList = []
            db, storeObj = shopifyOper.loadStore([])
            for j in data.index.values:
                df_line = data.loc[j, ['order_id','tracking_number','tracking_url','tracking_company','store_id']].to_dict()
                order_id = df_line['order_id']
                tracking_number = df_line['tracking_number']
                tracking_url = df_line['tracking_url']
                tracking_company = df_line['tracking_company']
                store = df_line['store_id']
                dictData = {'order_id': order_id, 'tracking_number': tracking_number, 'store': store,'tracking_url':tracking_url,'tracking_company':tracking_company}
                result = shopifyOper().uploadTracking(dictData,db,storeObj)
                if not result:
                    msg = '失败'
                else:
                    msg = '成功'
                resList.append(msg)
        else:
            return '文件类型不正确'
    return '上传状态：' + "\r\n".join(resList)






#. 判断文件类型
def check_file_type(filename):
    file_type = ['xls','xlsx','csv']
    # 获取文件后缀
    ext = filename.split('.')[1]
    # 判断文件是否是允许上传得类型
    if ext in file_type:
        return ext
    else:
        return False


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
    app.run(host='0.0.0.0',port=5000)

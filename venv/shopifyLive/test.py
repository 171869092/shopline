#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
import flask

app = Flask(__name__)
from shopifyLive.shopifyOper import *
@app.route('/')
def test():
    return shopApi()

# @app.route('test')
def shopApi():
    s = shopifyOper()
    s.pullOrder()
    return 'shopify api test pork'

if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    app.run()
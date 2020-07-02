#!/usr/bin/python
# -*- coding: utf-8 -*-
import time,json
import shopify
from datetime import datetime, timedelta
import random
import uuid
import pymysql
from pymysql.cursors import DictCursor

class shopifyOper:
    API_KEY = '16e1972ecb833997ee1fb2db724786d0'
    API_PASSWORD = '5799b2f7864a81082c954b36d0db3707'
    API_VERSION = '2020-04'
    API_NAME = 'animalsdreamde'
    API_SECRET = 'deab9706b878166122a28bea90db87ae'
    API_TOKEN = '6520467f8219236f0e98d99c39360719'
    SHOP_NAME = 'animalsdreamde'
    NAME = 'live'
    def __init__(self):
        """
        :keyword url: url
        :keyword shop_url: shop_url
        """
        self.url = ''
        self.shop_url =  "https://%s:%s@%s.myshopify.com/admin/api/%s" % (self.API_KEY, self.API_PASSWORD,self.API_NAME, self.API_VERSION)
        # self.shop_url = "https://%s.myshopify.com/admin" % ( self.SHOP_NAME)
        self.cursor = object
        self.db = object
    def pullOrder(self):
        """
        pull shopify oreder
        :return:
        """
        try:
            #. 读取店铺
            con,cursor = self.loadStore()
            if cursor and con:
                self.cursor = cursor
                self.db = con
            sql = "SELECT * FROM `store` WHERE status = 1"
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                return
            for data in results:
                shopify.ShopifyResource.set_user(data['api_key'])
                shopify.ShopifyResource.set_password(data['api_pwd'])
                shopUrl = "https://%s:%s@%s.myshopify.com/admin/api/%s" % (data['api_key'],data['api_pwd'],data['name'], data['api_version'])
                shopify.ShopifyResource.set_site(shopUrl)
                shopify.Shop.current()
                nowT = self.tsTime()
                strTime = self.formatTime(nowT)
                endT = self.endTime()
                endTime = self.formatTime(endT)
                # . 按时间匹配当日订单
                # order = shopify.Order().find(None, None, created_at_min=strTime, created_at_max=endTime)
                order = shopify.Order().find('2525433594015')
                data = []
                if isinstance(order, list):
                    for orders in order:
                        data.append(orders.to_dict())
                else:
                    data.append(order.to_dict())
                if order is None:
                    quit(0)
                self.execOrderDatas(data)
                # self.exportOrder(data)
        except Exception as e:
            raise e

    def execOrderDatas(self, data):
        """
        保存数据
        :return:
        """
        if not data:
            return
        curros = self.cursor
        db = self.db
        orderFormat = {}
        #. order
        self.insertOrder(data)
        # #. order_item
        # self.insertOrderItem(data)
        # #. order_shipping
        # self.insertOrderShipping(data)
        curros.close()
        db.close()
        return True

    def checkOrder(self,order_id, table):
        """
        check order
        :param data:
        :return:
        """
        if not order_id:
            return
        curros = self.cursor
        db = self.db
        sql = "SELECT * FROM `%s` WHERE order_id = %s" %(table,order_id)
        curros.execute(sql)
        results = curros.fetchone()
        return results

    def insertOrder(self,data):
        """
        insert order tables
        :param data:
        :return:
        """
        if not data:
            return
        curros = self.cursor
        db = self.db
        orderFormat = {}
        for i in data:
            orderFormat['order_id'] = i['id'];
            orderFormat['order_name'] = i['name']
            orderFormat['order_number'] = i['order_number']
            orderFormat['email'] = i['email']
            orderFormat['phone'] = i['phone']
            orderFormat['note'] = i['note']
            orderFormat['title'] = i['line_items'][0]['title']
            orderFormat['created_at'] = i['created_at']
            orderFormat['processed_at'] = i['processed_at']
            orderFormat['token'] = i['token']
            orderFormat['total_price'] = i['total_price']
            orderFormat['total_weight'] = i['total_weight']
            orderFormat['fulfillment_status'] = i['fulfillment_status']
            result = self.checkOrder(orderFormat['order_id'], 'order')
            if result:
                continue
            # values = ', '.join("'{}'".format(k) for k in orderFormat.values())
            insertOrder = "INSERT INTO `order` (`order_id`,`order_name`,`order_number`,`email`,`phone`,`note`,`title`,`created_at`,`processed_at`,`token`,`total_price`,`total_weight`,`fulfillment_status`) " \
                          "VALUES ('%s', '%s', '%s',' %s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s');" % (
                          orderFormat['order_id'], orderFormat['order_name'], orderFormat['order_number'],
                          orderFormat['email'], orderFormat['phone'], orderFormat['note'], orderFormat['title'],
                          orderFormat['created_at'], orderFormat['processed_at'], orderFormat['token'],
                          orderFormat['total_price'], orderFormat['total_weight'], orderFormat['fulfillment_status'])
            try:
                pass
                rs = curros.execute(insertOrder)
                print(rs)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
        return True

    def insertOrderItem(self,data):
        """
        insert order_item tables
        :param data:
        :return:
        """
        if not data:
            return
        curros = self.cursor
        db = self.db
        orderFormat = {}
        for i in data:
            for x in i['line_items']:
                orderFormat['order_id'] = i['id']
                orderFormat['title'] = i['line_items'][0]['title']
                orderFormat['quantity'] = x['quantity']
                orderFormat['sku'] = x['sku']
                orderFormat['name'] = x['name']
                result = self.checkOrder(orderFormat['order_id'], 'order_item')
                if result:
                    continue
                insertOrder = "INSERT INTO `order_item` (`order_id`,`title`,`quantity`,`sku`,`name`) " \
                              "VALUES ('%s', '%s', '%s',' %s', '%s');" % (
                                  orderFormat['order_id'], orderFormat['title'], orderFormat['quantity'],
                                  orderFormat['sku'], orderFormat['name'])
                try:
                    pass
                    rs = curros.execute(insertOrder)
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()


    def insertOrderShipping(self, data):
        """
        insert order_shipping tables
        :param data:
        :return:
        """
        if not data:
            return
        curros = self.cursor
        db = self.db
        orderFormat = {}
        for i in data:
            orderFormat['order_id'] = i['id']
            orderFormat['first_name'] = i['shipping_address']['first_name']
            orderFormat['last_name'] = i['shipping_address']['last_name']
            orderFormat['address1'] = i['shipping_address']['address1']
            orderFormat['address2'] = i['shipping_address']['address2']
            orderFormat['city'] = i['shipping_address']['city']
            orderFormat['zip'] = i['shipping_address']['zip']
            orderFormat['province'] = i['shipping_address']['province']
            orderFormat['country'] = i['shipping_address']['country']
            orderFormat['company'] = i['shipping_address']['company']
            orderFormat['latitude'] = i['shipping_address']['latitude']
            orderFormat['longitude'] = i['shipping_address']['longitude']
            orderFormat['name'] = i['shipping_address']['name']
            orderFormat['country_code'] = i['shipping_address']['country_code']
            orderFormat['province_code'] = i['shipping_address']['province_code']
            result = self.checkOrder(orderFormat['order_id'], 'shipping_detail')
            if result:
                continue
            insertOrder = "INSERT INTO `shipping_detail` (`order_id`,`first_name`,`last_name`,`address1`,`address2`,`city`,`zip`,`province`,`country`,`company`,`latitude`,`longitude`,`name`,`country_code`,`province_code`) " \
                          "VALUES ('%s', '%s', '%s',' %s', '%s', '%s' , '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                              orderFormat['order_id'], orderFormat['first_name'], orderFormat['last_name'],
                              orderFormat['address1'], orderFormat['address2'], orderFormat['city'] , orderFormat['zip'], orderFormat['province'], orderFormat['country'], orderFormat['company'],
                              orderFormat['latitude'],orderFormat['longitude'],orderFormat['name'] , orderFormat['country_code'], orderFormat['province_code'])
            try:
                pass
                rs = curros.execute(insertOrder)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
        return True
    def exportOrder(self, data):
        import csv
        import codecs
        import pandas
        import sys,io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
        """
        导出csv
        :param data:
        :return:
        """
        if not isinstance(data, list):
            return
        try:
            newList = []
            namespace = uuid.NAMESPACE_URL
            for x in data:
                uid = uuid.uuid3(namespace, self.NAME)
                newList.append({
                    'order_id' : str(x['id']),
                    'tracking_number': 'YT2018121272089185',
                    'email': x['email'],
                    'only_id': uid,
                    'currency':x['currency'],
                    'order_number' : x['order_number'],
                    'sku': x['line_items'][0]['sku'],
                    'title' :x['line_items'][0]['title'],
                    'quantity': x['line_items'][0]['quantity'],
                    'created_at': x['created_at'],
                    'phone': x['phone'],
                    'note': x['note'],
                    'shipping_address1': x['shipping_address']['address1'],
                    'shipping_address2': x['shipping_address']['address2'],
                    'shipping_address_first_name': x['shipping_address']['first_name'],
                    'shipping_address_last_name': x['shipping_address']['last_name'],
                    'shipping_address_city': x['shipping_address']['city'],
                    'shipping_address_country': x['shipping_address']['country'],
                    'shipping_address_latitude': x['shipping_address']['latitude'],
                    'shipping_address_name':x['shipping_address']['name'],
                    'shipping_address_zip': x['shipping_address']['zip'],
                })
            with open("E:\\livePython\\order%s.csv" % time.strftime("%Y-%m-%d-%H-%M"), 'w+', newline='',encoding='utf-8') as f:
                headers = ['order_id','tracking_number', 'email', 'only_id','currency','order_number','sku','title','quantity','created_at','phone','note','shipping_address1','shipping_address2',
                           'shipping_address_first_name','shipping_address_last_name','shipping_address_city','shipping_address_country','shipping_address_latitude','shipping_address_name','shipping_address_zip']
                csvrwite = csv.DictWriter(f, headers)
                csvrwite.writeheader()
                csvrwite.writerows(newList)
        except Exception as e:
            raise e
        return True

    def formatTime(self,timeStamp, zoor = '02:00'):
        localTime = time.localtime(timeStamp)
        strTime = time.strftime("%Y-%m-%dT%H:%M:%S+"+zoor, localTime)
        return strTime

    def tsTime(self):

        t = time.strftime("%Y-%m-%d 00:00:00", time.localtime())
        # 将其转换为时间数组
        timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳:
        timeStamp = int(time.mktime(timeStruct))
        return timeStamp

    def endTime(self):
        # t = "2020-06-27 23:59:59"
        t = time.strftime("%Y-%m-%d 23:59:59", time.localtime())
        # 将其转换为时间数组
        timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳:
        timeStamp = int(time.mktime(timeStruct))
        return timeStamp

    def tid_maker(self):
        return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1, 10)) for i in range(5)])



    def uploadTracking(self,data):
        """
        上传跟踪号
        :param data:
        :return:
        """
        try:
            if data['order_id'] and data['tracking_number'] is not None:
                quit(999)
            shopify.ShopifyResource.set_site(self.shop_url)
            fulfillment = shopify.Fulfillment.find_first(order_id=data['order_id'])
            fulfillment.tracking_number = [data['tracking_number']]
            fulfillment.save()
            return True
        except Exception as e:
            raise e

    def loadStore(self):
        """
        加载店铺
        :return:
        """
        db = pymysql.connect(host="3.236.55.209", user="root", password="wangke888", port=3306, database="shopify",
                             charset="utf8")
        cursor = db.cursor(DictCursor)
        return db,cursor
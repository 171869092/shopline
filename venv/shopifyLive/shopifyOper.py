#!/usr/bin/python
# -*- coding: utf-8 -*-
import time,json
import shopify
from datetime import datetime, timedelta
import random


class shopifyOper:
    API_KEY = '16e1972ecb833997ee1fb2db724786d0'
    API_PASSWORD = '5799b2f7864a81082c954b36d0db3707'
    API_VERSION = '2020-04'
    API_NAME = 'animalsdreamde'
    API_SECRET = 'deab9706b878166122a28bea90db87ae'
    API_TOKEN = '6520467f8219236f0e98d99c39360719'
    SHOP_NAME = 'animalsdreamde'
    def __init__(self):
        """
        :keyword url: url
        :keyword shop_url: shop_url
        """
        self.url = ''
        self.shop_url =  "https://%s:%s@%s.myshopify.com/admin/api/%s" % (self.API_KEY, self.API_PASSWORD,self.API_NAME, self.API_VERSION)
        self.shop_url = "https://%s.myshopify.com/admin" % ( self.SHOP_NAME)

    def pullOrder(self):
        """
        pull shopify oreder
        :return:
        """
        try:
            shopify.ShopifyResource.set_user(self.API_KEY)
            shopify.ShopifyResource.set_password(self.API_PASSWORD)
            shopify.ShopifyResource.set_site(self.shop_url)
            shopify.Shop.current()
            finds = shopify.Order().find()

            nowT = self.tsTime()
            strTime = self.formatTime(nowT)

            endT = self.endTime()
            endTime = self.formatTime(endT)

            # . 按时间匹配当日订单
            order = shopify.Order().find(None, None, created_at_min=strTime, created_at_max=endTime)
            # order = shopify.Order().find('2525433594015')
            data = []
            if isinstance(order, list):
                for orders in order:
                    data.append(orders.to_dict())
            else:
                data.append(order.to_dict())
            if order is None:
                quit(0)

            self.exportOrder(data)
        except Exception as e:
            raise e

    def exportOrder(self, data):
        import csv
        import codecs
        """
        导出csv
        :param data:
        :return:
        """
        if not isinstance(data, list):
            return
        try:
            print(data)
            # with open('E:\\livePython\\test.csv', 'wb') as f:
            #     write = csv.writer(f)
            #     write.writerows(11)
            #     print('完成')
        except Exception as e:
            raise e
        return True

    def formatTime(self,timeStamp, zoor = '02:00'):
        localTime = time.localtime(timeStamp)
        strTime = time.strftime("%Y-%m-%dT%H:%M:%S+"+zoor, localTime)

        return strTime

    def tsTime(self):
        t = "2020-06-27 00:00:00"
        # 将其转换为时间数组
        timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳:
        timeStamp = int(time.mktime(timeStruct))
        return timeStamp

    def endTime(self):
        t = "2020-06-27 23:59:59"
        # 将其转换为时间数组
        timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳:
        timeStamp = int(time.mktime(timeStruct))
        return timeStamp
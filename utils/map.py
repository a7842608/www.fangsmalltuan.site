# -*- coding: utf-8 -*-
# import pandas as pd
import json
import re
from urllib.request import urlopen, quote
import csv
import traceback
import os
# 构造获取经纬度的函数
import requests
from django.http import JsonResponse

'''通过地点拿到坐标值''' # 先那坐标入库, 然后拿库里的坐标取周边信息
def getlnglat(address):
    # http://api.map.baidu.com/geocoding/v3/?address=北京市海淀区上地十街10号&output=json&ak=您的ak&callback=showLocation //GET请求
    ak = '8RnUuaeOH6cGXMWk0VURz11mcsFylmy6'  # 需填入自己申请应用后生成的ak
    url = 'http://api.map.baidu.com/geocoding/v3/?address=%s&output=json&ak=%s&callback=showLocation' % (address, ak)
    req = requests.get(url).text
    try:
        a = req.split(',')
        b = a[1].split(':')
        c = a[2].replace('}', '').split(':')
        print('lng', b[-1])
        print('lat', c[-1])
        data = {'lng':b[-1], 'lat': c[-1]}
        return data
    except Exception as e:
        return e

# http://api.map.baidu.com/place/v2/search?query=银行&location=39.915,116.404&radius=2000&output=xml&ak=您的密钥 //GET请求


'''获取周边配套'''
def surrounding_facility(query, location):
    access_token = '8RnUuaeOH6cGXMWk0VURz11mcsFylmy6'
    url = 'http://api.map.baidu.com/place/v2/search?query={}&location={}&radius=5000&output=json&ak={}'.format(query,location,access_token)
    # url = 'http://api.map.baidu.com/place/v2/search?query=%E9%93%B6%E8%A1%8C&location=39.915,116.404&radius=2000&output=json&ak=8RnUuaeOH6cGXMWk0VURz11mcsFylmy6'
    response = requests.get(url)
    try:
        return response.json()
    except Exception as e:
        return e
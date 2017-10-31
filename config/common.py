# -*- coding: utf-8 -*-
# @Author: xiyou_zlg
# @Date:   2017-09-21 13:59:36
# @Last Modified by:   xiyou_zlg
# @Last Modified time: 2017-09-25 15:14:42

import urllib
import urllib.parse
import urllib.request
import socket
import requests

from collections import OrderedDict
from pyexcel_xls import get_data
from pyexcel_xls import save_data

# 上传天猫图片
def api_tmall_img(name, img_url):
    # url = 'http://cha.aliapi.com/api/v0/attrimg' # 本地
    # url = 'http://ali.shoplinq.cn/api/v0/attrimg' # 线上
    url = 'http://192.168.142.1/api/v0/attrimg'
    params = { 'img_channel' : 'tmall_abroad', 'img_name' : name, 'img_src' : img_url } # 线上运行
    data = urllib.parse.urlencode(params).encode('utf-8')
    request = urllib.request.Request(url)
    request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    f = urllib.request.urlopen(request, data)
    return f.read().decode('utf-8')


# 保存xls文件到指定路径
def save_xls(path, name, title, datalist):
    data = OrderedDict()
    sheet_1 = []
    sheet_1.append(title)
    for item in datalist:
        sheet_1.append(item)
    data.update({name : sheet_1})
    save_data(path, data)

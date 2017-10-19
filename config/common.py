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
    user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1)'
    params = { 'img_channel' : 'tmall_abroad', 'img_name' : name, 'img_src' : img_url } # 线上运行
    headers = { 'User-Agent' : user_agent }
    data = urllib.parse.urlencode(params).encode(encoding='utf-8')
    req = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(req)
    return response.read()


# 保存xls文件到指定路径
def save_xls(path, name, title, datalist):
    data = OrderedDict()
    sheet_1 = []
    sheet_1.append(title)
    for item in datalist:
        sheet_1.append(item)
    data.update({name : sheet_1})
    save_data(path, data)

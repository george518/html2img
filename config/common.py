# -*- coding: utf-8 -*-
# @Author: xiyou_zlg
# @Date:   2017-09-21 13:59:36
# @Last Modified by:   xiyou_zlg
# @Last Modified time: 2017-09-25 15:14:42

import urllib
import urllib.parse
import urllib.request
import socket
import re
import os

from collections import OrderedDict
from pyexcel_xls import get_data
from pyexcel_xls import save_data

# 上传天猫图片
def api_tmall_img(name, img_url):
    url = 'http://cha.aliapi.com/api/v0/image'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    params = { 'img_channel' : 'tmall_abroad', 'img_name' : name, 'img_src' : img_url } # 线上运行
    headers = { 'User-Agent' : user_agent }
    data = urllib.parse.urlencode(params).encode(encoding='UTF8')
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

# 获取hostIP
def get_ip():
    localIP = socket.gethostbyname(socket.gethostname())
    return localIP

def get_test_ip():
    try:
        myip = visit("http://whois.pconline.com.cn")   #visit访问节点
    except:
        try:
            myip = visit("http://www.net.cn/static/customercare/yourip.asp")
        except:
            try:
                myip = visit("http://ip.chinaz.com/getip.aspx")
            except:
                myip = '0'
    return myip

def visit(url):
        urler = urllib.parse.urlparse(url)
        if url == urler.geturl():
            opener = urllib.request.urlopen(url)     
            strg = opener.read()
            strg = strg.decode('gbk')
        ipaddr = re.search('\d+\.\d+\.\d+\.\d+',strg).group(0)
        location = re.search(r"(.*)市(.*)",strg).group(0)
        location = location.expandtabs(1)
        return ipaddr
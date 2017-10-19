# -*- coding: utf-8 -*-
# @Author: haodaquan
# @Date:   2017-08-21 17:19:28
# @Last Modified by:   xiyou_zlg
# @Last Modified time: 2017-09-25 15:32:06

import os.path
import time
import zipfile
import json
import base64

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask import send_file
from flask import make_response
from flask import Response

from config.common import *
from config.mysql import Mysql
from pyexcel_xls import get_data
from pyexcel_xls import save_data
from collections import OrderedDict
from werkzeug.utils import secure_filename


app = Flask(__name__)

# 定义文件下载和上传地址
ZIP_FOLDER = 'uploads/zip'
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'download'
ALLOWED_EXTENSIONS = set(['xlsx','zip'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ZIP_FOLDER'] = ZIP_FOLDER

# 判断允许的文件类型


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 属性图首页


@app.route('/')
def index():
    return render_template('upload.html')

# 下载模板


@app.route('/download/<path:filename>')
def download_file(filename):
    dirpath = os.path.join(app.root_path, DOWNLOAD_FOLDER)
    return send_from_directory(dirpath, filename, as_attachment=True)

# 上传文件


@app.route('/upload', methods=['POST'], strict_slashes=False)
def upload_file():
    basedir = app.root_path
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值

    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = fname.rsplit(
            '.', 1)[0] + '__' + str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        return redirect("/show/"+new_filename)
    else:
        abort(404)


# 显示excel图片

@app.route('/show/<path:filename>', methods=['GET'], strict_slashes=False)
def showTable(filename):
    basedir   = app.root_path
    excelName = filename  # 判断文件是否存在
    file_dir  = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    excelPath = file_dir + "/" + excelName
    xls_data_ = get_data(excelPath)

    for sheet_n in xls_data_.keys():
        xls_title = xls_data_[sheet_n][0]
        xls_data = xls_data_[sheet_n]

    # 处理表头
    title = {}
    itemsCount = 0
    for k, v in enumerate(xls_data[0]):
        if k > 4:
            d = {}
            d['name'] = v.rsplit('-', 1)[0]
            d['col'] = int(v.rsplit('-', 1)[1])
            title[k] = d
            itemsCount = k

    itemsCount = itemsCount + 1
    data = {}
    data['title'] = title
    data['attrs'] = xls_data[1:]
    data['count'] = len(xls_data[1:])
    data['itcount'] = itemsCount

    return render_template('show.html', data=data)

# 上传图片
@app.route('/tmall_img')
def tmall_img():
    return render_template('tmall_img.html')


# zip图片包处理
@app.route('/upload_imgs', methods=['POST'], strict_slashes=False)
def upload_zip_file():
    basedir = app.root_path
    fsp_dir = os.path.join(basedir, app.config['ZIP_FOLDER']) # zip地址

    if not os.path.exists(fsp_dir):
        os.makedirs(fsp_dir)

    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值

    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = fname.rsplit('.', 1)[0] + '__' + str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(fsp_dir, new_filename))  # 保存文件到upload目录
        return redirect("/send_tmall_imgs/"+new_filename)
    else:
        abort(404)


# 想接口处理图片
@app.route('/send_tmall_imgs/<path:filename>', methods=['GET'], strict_slashes=False)
def upload_tamll(filename):
    basedir   = app.root_path
    zipName = filename  # 判断文件是否存在
    file_dir  = os.path.join(basedir, app.config['ZIP_FOLDER'])
    date = time.strftime("%Y-%m-%d")
    zipPath = file_dir + "/" + zipName
    ezipPath = os.path.join(file_dir, zipName.replace('.zip','')) # 解压出来临时存放目录

    hostIP = url_for('index', _external=True)

    if not os.path.exists(ezipPath):
        os.makedirs(ezipPath)

    data = []
    hr = zipfile.is_zipfile(zipPath)
    if hr:
        fz = zipfile.ZipFile(zipPath, 'r')
        flist = fz.namelist()
        for f in flist:
            fz.extract(f, ezipPath)
            ne = f.split(".")
            name = ne[0]+'.jpg' # 图片名称
            # 向天猫传图
            img_url = "{0}{1}/{2}".format(hostIP.replace('5000','81'), zipName.replace('.zip',''), f) # 线上
            json_res = api_tmall_img(name, img_url)
            res = json.loads(json_res)
            tmall_url = res['data'] #上传天猫后图片地址
            data.append((name, tmall_url))
            
            # os.remove(os.path.join(ezipPath, f)) #暂时不删除图片
        fz.close()
    # os.rmdir(ezipPath) #暂时不删除图片
    # os.remove(zipPath) #暂时不删除图片
    db = Mysql()
    for item in data:
        sql = " insert into ali_attr_img (name,ali_src,date) values('{0}','{1}','{2}') ".format(item[0], item[1], date)
        db.add(sql)
    return redirect("/cdnimglist")


# 蹄片列表展示
@app.route('/cdnimglist')
def cdnimglist():
    date = time.strftime("%Y-%m-%d")
    db = Mysql()
    lins = db.select(" select * from ali_attr_img where date = '{0}' ".format(date))
    return render_template('imglist.html', list=lins)


# 保存列表数据
@app.route('/download_img')
def download_img():
    date = time.strftime("%Y-%m-%d")
    unix_time = int(time.time())
    db = Mysql()
    lins = db.select(" select * from ali_attr_img where date = '{0}' ".format(date))
    name = '天猫图片_' + str(unix_time) + '.xls'
    title = (u'编号', u'名称', u'图片地址', u'日期')
    dirpath = os.path.join(app.root_path, ZIP_FOLDER, name)
    save_xls(dirpath, name, title, lins)
    directory = os.path.join(app.root_path, ZIP_FOLDER)
    response = make_response(send_from_directory(directory, name, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={0}".format(name.encode().decode('latin-1'))
    return response


# 获取展示图片地址
@app.route('/image/<path:filename>', methods=['GET'], strict_slashes=False)
def show_img(filename):
    basedir = app.root_path
    pth = filename.split("|")
    imgpath = os.path.join(basedir, app.config['ZIP_FOLDER'], pth[0], pth[1])
    h = open(imgpath,'rb')
    image_data = base64.b64encode(h.read())
    h.close()
    return Response(base64.b64decode(image_data) , mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=8888)

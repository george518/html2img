# -*- coding: utf-8 -*-
# @Author: haodaquan
# @Date:   2017-08-21 17:19:28
# @Last Modified by:   haodaquan
# @Last Modified time: 2017-08-22 23:43:37

import os.path
import time

from collections import OrderedDict
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from pyexcel_xls import get_data
from pyexcel_xls import save_data
from werkzeug.utils import secure_filename


app = Flask(__name__)

# 定义文件下载和上传地址
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'download'
ALLOWED_EXTENSIONS = set(['xlsx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=8888)

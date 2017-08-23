# @Author: haodaquan
# @Date:   2017-08-21 17:19:28
# @Last Modified by:   haodaquan
# @Last Modified time: 2017-08-22 23:43:37

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from upload import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)  # flask默认的端口
IOLoop.instance().start()
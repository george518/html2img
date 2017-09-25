# -*- coding: utf-8 -*-
# @Author: xiyou_zlg
# @Date:   2017-09-22 13:19:25
# @Last Modified by:   xiyou_zlg
# @Last Modified time: 2017-09-22 17:06:33

import mysql.connector

class Mysql(object):
    def __init__(self):
        self.__host = '127.0.0.1'
        self.__username = 'root'
        self.__password = '123456'
        self.__database = 'test'
        self.__port = '3306'
        self.__db = mysql.connector.connect(host=self.__host,user=self.__username, password=self.__password, database=self.__database, port=self.__port)

    def add(self, sql):
        db = self.__db
        cursor = db.cursor() # 使用cursor()方法获取操作游标
        try:
            cursor.execute(sql) # 执行sql语句
            db.commit() # 提交到数据库执行
        except Exception as e:
            db.rollback()
        # db.close() # 关闭数据库连接


    def select(self, sql):
        db = self.__db
        cursor = db.cursor()
        results = []
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except Exception as e:
            print("Error: unable to fecth data")
        # db.close()
        return results


    def update(self, sql):
        db = self.__db
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
        # db.close()


    def delete(self, sql):
        db = self.__db
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
        # db.close()
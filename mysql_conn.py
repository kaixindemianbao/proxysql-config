#!/usr/bin/python3
import random
import pymysql
class SQLgo():
    def __init__(self, ip=None, user=None, password=None , db=None, port=None):
        self.ip = ip
        self.user = user
        self.db = db
        self.port = int(port)
        self.password=password
        self.con =  pymysql.connect(
            host=self.ip,
            user=self.user,
            passwd=self.password,
            db=self.db,
            charset='utf8mb4',
            port=self.port
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def exec(self, sql=None):
        with self.con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    def save_config(self):
      list1=['load mysql servers to runtime','save mysql servers to disk','load mysql users to runtime','save mysql users to disk','load mysql query rules to runtime','save mysql query rules to disk']
      with self.con.cursor() as cursor:
        for i in list1:
          cursor.execute(i)
          result = cursor.fetchall()
    def save_variables(self):
      list1=['load mysql variables to runtime','save mysql variables to disk']
      with self.con.cursor() as cursor:
       for i in list1:
         cursor.execute(i)
         result = cursor.fetchall()
    def qingli(self):
      list1=['delete from mysql_servers','delete from mysql_users','delete from mysql_query_rules']
      with self.con.cursor() as cursor:
        for i in list1:
          cursor.execute(i)
          result = cursor.fetchall()
        self.save_config()
  




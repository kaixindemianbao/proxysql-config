#!/usr/bin/python3
import ConfigParser
from mysql_conn import *
conf = ConfigParser.ConfigParser()
conf.read("config.txt")
c={}
def common(var):
   sections = conf.options(var)
   for i in sections:
     c[i]=conf.get(var,i)
   return c
def peizhi():
  c=common('server_config')
  d=[]
  sql1="insert into mysql_servers(hostgroup_id,hostname,port,weight,max_connections,max_replication_lag,comment) values(%s,'%s',%s,%s,%s,%s,'%s');" %(int(c['w-hostgroupid']),c['master'].split(':')[0],c['master'].split(':')[1],c['w-weight'],c['max_connections'],c['max_replication_lag'],c['w-comment'])
  for i in c['slave'].split(','):
    sql2="insert into mysql_servers(hostgroup_id,hostname,port,weight,max_connections,max_replication_lag,comment) values(%s,'%s',%s,%s,%s,%s,'%s');" %(int(c['r-hostgroupid']),i.split(':')[0],i.split(':')[1],c['r-weight'],c['max_connections'],c['max_replication_lag'],c['r-comment'])
    d.append(sql2)
  sql3="INSERT INTO mysql_users(username,password,active,default_hostgroup,transaction_persistent)values('%s','%s',1,'%s',1);" %(c['w-user'],c['w-password'],int(c['w-hostgroupid']))
  sql4="INSERT INTO mysql_query_rules(active,match_pattern,destination_hostgroup,apply) VALUES(1,'^SELECT.*FOR UPDATE$',%s,1);" %(int(c['w-hostgroupid']))
  sql5="INSERT INTO mysql_query_rules(active,match_pattern,destination_hostgroup,apply)VALUES(1,'^SELECT',%s,1);" %(int(c['r-hostgroupid']))
  d.append(sql1)
  d.append(sql3)
  d.append(sql4)
  d.append(sql5)
  cc=SQLgo('127.0.0.1','admin','admin','main','6032')
  for i in d:
    cc.exec(i)
  cc.save_config()
def peizhi2():
  c1=common('common')
  sql1="set mysql-max_connections=%s" %(c1['mysql-max_connections'])
  sql2="set mysql-monitor_slave_lag_when_null=%s" %(c1['mysql-monitor_slave_lag_when_null'])
  sql3="set mysql-monitor_username='%s'" %(c1['mysql-monitor_username'])
  sql4="set mysql-monitor_password='%s'" %(c1['mysql-monitor_password'])
  cc=SQLgo('127.0.0.1','admin','admin','main','6032')
  cc.exec(sql1)
  cc.exec(sql2)
  cc.exec(sql3)
  cc.exec(sql4)
  cc.save_variables()
  print("创建监控账号") 
  print("GRANT SUPER,REPLICATION CLIENT ON *.* TO '%s' IDENTIFIED BY '%s'" %(c1['mysql-monitor_username'],c1['mysql-monitor_password']))
def qingli():
  cc=SQLgo('127.0.0.1','admin','admin','main','6032')
  cc.qingli()
peizhi()

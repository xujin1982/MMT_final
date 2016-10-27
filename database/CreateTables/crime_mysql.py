# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 09:07:13 2016

@author: Junxiao
"""

#!/usr/bin/python


import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost","root","123456789o","MMT" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS crime")

# 创建数据表SQL语句
sql = """CREATE TABLE crime (
         GEOID  INT NOT NULL primary key,
         Murder float,
         Rape float,
         Robbery float,
         Assault float,
         Violent_crime float,
         Burglary float,
         Theft float,
         Vehicle_theft float,
         Property_crime float,
         Law_enforcement_employees float,
         Police_officers float,
         Violent_1_years_ago float,
         Property_1_years_ago float,
         Crime_1_years_ago float,         
         Murder_boolean int,
         Rape_boolean int,
         Robbery_boolean int,
         Assault_boolean int,
         Violent_crime_boolean int,
         Burglary_boolean int,
         Theft_boolean int,
         Vehicle_theft_boolean int,
         Property_crime_boolean int,
         Law_enforcement_employees_boolean int,
         Police_officers_boolean int,
         Violent_1_years_ago_boolean int,
         Property_1_years_ago_boolean int,
         Crime_1_years_ago_boolean int)"""

cursor.execute(sql)

# 关闭数据库连接
db.close()

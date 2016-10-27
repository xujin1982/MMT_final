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
cursor.execute("DROP TABLE IF EXISTS weather")

# 创建数据表SQL语句
sql = """CREATE TABLE weather (
         GEOID  INT NOT NULL primary key,
         January_min float,
         February_min float,
         March_min float,
         April_min float,
         May_min float,
         June_min float,
         July_min float,
         August_min float,
         September_min float,
         October_min float,
         November_min float,
         December_min float,
         January_max float,
         February_max float,
         March_max float,
         April_max float,
         May_max float,
         June_max float,
         July_max float,
         August_max float,
         September_max float,
         October_max float,
         November_max float,
         December_max float,
         January_avg float,
         February_avg float,
         March_avg float,
         April_avg float, 
         May_avg float,  
         June_avg float,
         July_avg float,
         August_avg float,
         September_avg float, 
         October_avg float,
         November_avg float,
         December_avg float,
         Air_quality_index float,
         Pollution_index float,
         Days_measured float,
         Days_with_good_air_quality float,
         Days_with_moderate_air_quality float,
         Days_w_poor_A_Q_for_sensitive_groups float,
         Days_with_unhealthy_air_quality float,
         Arsenic float,
         Benzene float,
         Carbon_Tetrachloride float,
         Lead float,
         Mercury float,         
         January_min_boolean int,
         February_min_boolean int,
         March_min_boolean int,
         April_min_boolean int,
         May_min_boolean int,
         June_min_boolean int,
         July_min_boolean int,
         August_min_boolean int,
         September_min_boolean int,
         October_min_boolean int,
         November_min_boolean int,
         December_min_boolean int,
         January_max_boolean int,
         February_max_boolean int,
         March_max_boolean int,
         April_max_boolean int,
         May_max_boolean int,
         June_max_boolean int,
         July_max_boolean int,
         August_max_boolean int,
         September_max_boolean int,
         October_max_boolean int,
         November_max_boolean int,
         December_max_boolean int,
         January_avg_boolean int,
         February_avg_boolean int,
         March_avg_boolean int,
         April_avg_boolean int, 
         May_avg_boolean int,  
         June_avg_boolean int,
         July_avg_boolean int,
         August_avg_boolean int,
         September_avg_boolean int, 
         October_avg_boolean int,
         November_avg_boolean int,
         December_avg_boolean int,
         Air_quality_index_boolean int,
         Pollution_index_boolean int,
         Days_measured_boolean int,
         Days_with_good_air_quality_boolean int,
         Days_with_moderate_air_quality_boolean int,
         Days_w_poor_A_Q_for_sensitive_groups_boolean int,
         Days_with_unhealthy_air_quality_boolean int,
         Arsenic_boolean int,
         Benzene_boolean int,
         Carbon_Tetrachloride_boolean int,
         Lead_boolean int,
         Mercury_boolean int)"""

cursor.execute(sql)

# 关闭数据库连接
db.close()

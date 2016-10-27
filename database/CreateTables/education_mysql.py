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
cursor.execute("DROP TABLE IF EXISTS education")

# 创建数据表SQL语句
sql = """CREATE TABLE education (
         GEOID  INT NOT NULL primary key,
         Average_Test_Scores float,
         Student_Teacher_ratio float,
         Total_public_schools float,
         Total_private_schools float,
         Total_post_secondary_schools float,
         Completed_8th_grade float,
         Completed_high_school float,
         Completed_some_college float,
         Completed_associate_degree float,
         Completed_bachelors float,
         Completed_masters float,
         Completed_professional_degree float,
         Completed_doctorate float,
         High_school_diploma_Male float,
         Some_college_Male float,
         Associates_degree_Male float,
         Professional_schooling_Male float,
         Bachelors_degree_Male float,
         Masters_degree_Male float,
         Doctorate_degree_Male float,
         High_school_diploma_Female float,
         Some_college_Female float,
         Associates_degree_Female float,
         Professional_schooling_Female float,
         Bachelors_degree_Female float,
         Masters_degree_Female float,
         Doctorate_degree_Female float,         
         Average_Test_Scores_boolean int,
         Student_Teacher_ratio_boolean int,
         Total_public_schools_boolean int,
         Total_private_schools_boolean int,
         Total_post_secondary_schools_boolean int,
         Completed_8th_grade_boolean int,
         Completed_high_school_boolean int,
         Completed_some_college_boolean int,
         Completed_associate_degree_boolean int,
         Completed_bachelors_boolean int,
         Completed_masters_boolean int,
         Completed_professional_degree_boolean int,
         Completed_doctorate_boolean int,
         High_school_diploma_Male_boolean int,
         Some_college_Male_boolean int,
         Associates_degree_Male_boolean int,
         Professional_schooling_Male_boolean int,
         Bachelors_degree_Male_boolean int,
         Masters_degree_Male_boolean int,
         Doctorate_degree_Male_boolean int,
         High_school_diploma_Female_boolean int,
         Some_college_Female_boolean int,
         Associates_degree_Female_boolean int,
         Professional_schooling_Female_boolean int,
         Bachelors_degree_Female_boolean int,
         Masters_degree_Female_boolean int,
         Doctorate_degree_Female_boolean int)"""

cursor.execute(sql)

# 关闭数据库连接
db.close()

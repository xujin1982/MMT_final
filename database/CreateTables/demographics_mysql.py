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
cursor.execute("DROP TABLE IF EXISTS demographics")

# 创建数据表SQL语句
sql = """CREATE TABLE demographics (
         GEOID  INT NOT NULL primary key,
         Population float,
         Population_density float,
         Median_age float,
         Male_Female_ratio float,
         Married float,
         Caucasian float,
         African_American float,
         Asian float,
         American_Indian float,
         Native_Hawaiian float,
         Mixed_race float,
         Other_race float,
         Hispanic_or_Latino_origin float,
         Speak_English float,
         Speak_Spanish float,
         Other_language float,
         In_state_of_res_BORN float,
         Out_of_state_BORN float,
         Out_of_US_BORN float,
         Foreign_BORN float,
         USD200K_plus float,
         USD150K_USD200K float,
         USD100K_USD150K float,
         USD60K_USD100K float,
         USD40K_USD60K float,
         USD25K_USD40K float,
         USD10K_USD25K float,
         USD10K_or_less float,
         Salary float,
         Self_Emp float,
         Investments float,
         Social_Sec float,
         Supplmental_Sec float,
         Public_Asst float,
         Retirment_Inc float,
         Other_income float,
         LESS5_Male float,
         5_14_Male float,
         15_19_Male float,
         20_24_Male float,
         25_34_Male float,
         35_44_Male float,
         45_54_Male float,
         55_64_Male float,
         65_84_Male float,
         GREATER85_Male float, 
         LESS5_Female float,  
         5_14_Female float, 
         15_19_Female float, 
         20_24_Female float,
         25_34_Female float, 
         35_44_Female float, 
         45_54_Female float, 
         55_64_Female float,
         65_84_Female float,
         GREATER85_Female float,
         Never_Male float,  
         Married_Male float, 
         Separated_Male float, 
         Divorced_Male float,  
         Widowed_Male float,
         Never_Female float,
         Married_Female float,  
         Separated_Female float,
         Divorced_Female float, 
         Widowed_Female float,
         Younger_than_6_only float,
         Both_younger_than_6_between_6_and_17 float,
         6_to_17_only float,         
         Population_boolean int,
         Population_density_boolean int,
         Median_age_boolean int,
         Male_Female_ratio_boolean int,
         Married_boolean int,
         Caucasian_boolean int,
         African_American_boolean int,
         Asian_boolean int,
         American_Indian_boolean int,
         Native_Hawaiian_boolean int,
         Mixed_race_boolean int,
         Other_race_boolean int,
         Hispanic_or_Latino_origin_boolean int,
         Speak_English_boolean int,
         Speak_Spanish_boolean int,
         Other_language_boolean int,
         In_state_of_res_BORN_boolean int,
         Out_of_state_BORN_boolean int,
         Out_of_US_BORN_boolean int,
         Foreign_BORN_boolean int,
         USD200K_plus_boolean int,
         USD150K_USD200K_boolean int,
         USD100K_USD150K_boolean int,
         USD60K_USD100K_boolean int,
         USD40K_USD60K_boolean int,
         USD25K_USD40K_boolean int,
         USD10K_USD25K_boolean int,
         USD10K_or_less_boolean int,
         Salary_boolean int,
         Self_Emp_boolean int,
         Investments_boolean int,
         Social_Sec_boolean int,
         Supplmental_Sec_boolean int,
         Public_Asst_boolean int,
         Retirment_Inc_boolean int,
         Other_income_boolean int,
         LESS5_Male_boolean int,
         5_14_Male_boolean int,
         15_19_Male_boolean int,
         20_24_Male_boolean int,
         25_34_Male_boolean int,
         35_44_Male_boolean int,
         45_54_Male_boolean int,
         55_64_Male_boolean int,
         65_84_Male_boolean int,
         GREATER85_Male_boolean int, 
         LESS5_Female_boolean int,  
         5_14_Female_boolean int, 
         15_19_Female_boolean int, 
         20_24_Female_boolean int,
         25_34_Female_boolean int, 
         35_44_Female_boolean int, 
         45_54_Female_boolean int, 
         55_64_Female_boolean int,
         65_84_Female_boolean int,
         GREATER85_Female_boolean int,
         Never_Male_boolean int,  
         Married_Male_boolean int, 
         Separated_Male_boolean int, 
         Divorced_Male_boolean int,  
         Widowed_Male_boolean int,
         Never_Female_boolean int,
         Married_Female_boolean int,  
         Separated_Female_boolean int,
         Divorced_Female_boolean int, 
         Widowed_Female_boolean int,
         Younger_than_6_only_boolean int,
         Both_younger_than_6_between_6_and_17_boolean int,
         6_to_17_only_boolean int)"""

cursor.execute(sql)

# 关闭数据库连接
db.close()

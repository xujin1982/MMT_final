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
cursor.execute("DROP TABLE IF EXISTS cost_of_living")

# 创建数据表SQL语句
sql = """CREATE TABLE cost_of_living (
         GEOID  INT NOT NULL primary key,
         Household  float,
         Owners float,
         Renters float,
         General_Sales_Tax float,  
         With_Max_Surtax float,
         Income_Tax_Low float,
         Income_Tax_High float,
         Haircut float,
         Beauty_Salon float,
         Toothpaste float,
         Shampoo float,
         Movie float,
         Bowling float,
         Ground_Beef float,
         Fried_Chicken float,
         Milk float,
         Potatoes float,
         Pizza float,
         Beer float,
         Optometrist float,
         Doctor float,
         Dentist float,
         Ibuprofen float,
         Lipitor float,
         Home_Price float,
         Avg_Mortgage_Payment float,
         Apartment_Rent float,
         Gasoline float,
         Tire_Balancing float,
         All_Electricity float,
         Phone float,         
         Household_boolean int,
         Owners_boolean int,
         Renters_boolean int,
         General_Sales_Tax_boolean int,  
         With_Max_Surtax_boolean int,
         Income_Tax_Low_boolean int,
         Income_Tax_High_boolean int,
         Haircut_boolean int,
         Beauty_Salon_boolean int,
         Toothpaste_boolean int,
         Shampoo_boolean int,
         Movie_boolean int,
         Bowling_boolean int,
         Ground_Beef_boolean int,
         Fried_Chicken_boolean int,
         Milk_boolean int,
         Potatoes_boolean int,
         Pizza_boolean int,
         Beer_boolean int,
         Optometrist_boolean int,
         Doctor_boolean int,
         Dentist_boolean int,
         Ibuprofen_boolean int,
         Lipitor_boolean int,
         Home_Price_boolean int,
         Avg_Mortgage_Payment_boolean int,
         Apartment_Rent_boolean int,
         Gasoline_boolean int,
         Tire_Balancing_boolean int,
         All_Electricity_boolean int,
         Phone_boolean int)"""

cursor.execute(sql)

# 关闭数据库连接
db.close()

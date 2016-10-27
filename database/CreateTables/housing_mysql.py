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
cursor.execute("DROP TABLE IF EXISTS housing")

# 创建数据表SQL语句
sql = """CREATE TABLE housing (
         GEOID  INT NOT NULL primary key,
         Median_home_price float,
         Median_rent_asked float,
         Avg_people_per_household float,
         Owner_occupied_households float,
         Renter_occupied_households float,
         Occupied float,
         Vacant float,
         For_rent float,
         For_sale_only float,
         Rented_Sold_not_occ float,
         Seasonal float,
         Migrant_workers float,
         Other_occ float,
         Avg_household_size float,
         Avg_household_size_owner_occ float,
         Avg_household_size_renter_occ float,
         Median_house_hold_rooms float,
         Utility_gas float,
         Electricity float,
         Oil_or_kerosene float,
         Solar float,
         Other_heat float,
         None_heat float,
         0_9per float,
         10_19per float,
         20_29per float,
         30_39per float,
         40_49per float,
         50per_plus float,
         N_A float,
         Utilities_extra float,
         Utilities_included float,         
         Median_home_price_boolean int,
         Median_rent_asked_boolean int,
         Avg_people_per_household_boolean int,
         Owner_occupied_households_boolean int,
         Renter_occupied_households_boolean int,
         Occupied_boolean int,
         Vacant_boolean int,
         For_rent_boolean int,
         For_sale_only_boolean int,
         Rented_Sold_not_occ_boolean int,
         Seasonal_boolean int,
         Migrant_workers_boolean int,
         Other_occ_boolean int,
         Avg_household_size_boolean int,
         Avg_household_size_owner_occ_boolean int,
         Avg_household_size_renter_occ_boolean int,
         Median_house_hold_rooms_boolean int,
         Utility_gas_boolean int,
         Electricity_boolean int,
         Oil_or_kerosene_boolean int,
         Solar_boolean int,
         Other_heat_boolean int,
         None_heat_boolean int,
         0_9per_boolean int,
         10_19per_boolean int,
         20_29per_boolean int,
         30_39per_boolean int,
         40_49per_boolean int,
         50per_plus_boolean int,
         N_A_boolean int,
         Utilities_extra_boolean int,
         Utilities_included_boolean int)"""

cursor.execute(sql)

# 关闭数据库连接
db.close()

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
cursor.execute("DROP TABLE IF EXISTS employment")

# 创建数据表SQL语句
sql = """CREATE TABLE employment (
         GEOID  INT NOT NULL primary key,
         Income_per_capita float,
         Median_household_income float,
         Median_income_owner_occupied float,
         Median_income_renter_occupied float,
         Median_earnings_male float,
         Median_earnings_female float,
         Unemployment_rate float,
         Poverty_level float,
         Construction_industry_Male float,
         Manufacturing_sector_Male float,
         Financial_insurance_services_Male float,
         Wholesale_retail_services_Male float,
         Public_administration_Male float,
         Transportation_warehousing_utilities_Male float,
         Education_health_social_services_Male float,
         Other_employment_Male float,
         Construction_industry_Female float,
         Manufacturing_sector_Female float,
         Financial_insurance_services_Female float,
         Wholesale_retail_services_Female float,
         Public_administration_Female float,
         Transportation_warehousing_utilities_Female float,
         Education_health_social_services_Female float,
         Other_employment_Female float,
         In_labor_force float,
         Military float,
         Unemployed float,
         Unknown_Other float,
         35_hours_plus_Male float,
         34_to_15_hours_Male float,
         14_to_1_hours_Male float,
         None_Male float,
         35_hours_plus_Female float,
         34_to_15_hours_Female float,
         14_to_1_hours_Female float,
         None_Female float,
         0_10k_Male float,
         10k_25k_Male float,
         25k_40k_Male float,
         40k_65k_Male float,
         65k_100k_Male float,
         100k_plus_Male float,
         0_10k_Female float,
         10k_25k_Female float,
         25k_40k_Female float,
         40k_65k_Female float,
         65k_100k_Female float,
         100k_plus_Female float,         
         Income_per_capita_boolean int,
         Median_household_income_boolean int,
         Median_income_owner_occupied_boolean int,
         Median_income_renter_occupied_boolean int,
         Median_earnings_male_boolean int,
         Median_earnings_female_boolean int,
         Unemployment_rate_boolean int,
         Poverty_level_boolean int,
         Construction_industry_Male_boolean int,
         Manufacturing_sector_Male_boolean int,
         Financial_insurance_services_Male_boolean int,
         Wholesale_retail_services_Male_boolean int,
         Public_administration_Male_boolean int,
         Transportation_warehousing_utilities_Male_boolean int,
         Education_health_social_services_Male_boolean int,
         Other_employment_Male_boolean int,
         Construction_industry_Female_boolean int,
         Manufacturing_sector_Female_boolean int,
         Financial_insurance_services_Female_boolean int,
         Wholesale_retail_services_Female_boolean int,
         Public_administration_Female_boolean int,
         Transportation_warehousing_utilities_Female_boolean int,
         Education_health_social_services_Female_boolean int,
         Other_employment_Female_boolean int,
         In_labor_force_boolean int,
         Military_boolean int,
         Unemployed_boolean int,
         Unknown_Other_boolean int,
         35_hours_plus_Male_boolean int,
         34_to_15_hours_Male_boolean int,
         14_to_1_hours_Male_boolean int,
         None_Male_boolean int,
         35_hours_plus_Female_boolean int,
         34_to_15_hours_Female_boolean int,
         14_to_1_hours_Female_boolean int,
         None_Female_boolean int,
         0_10k_Male_boolean int,
         10k_25k_Male_boolean int,
         25k_40k_Male_boolean int,
         40k_65k_Male_boolean int,
         65k_100k_Male_boolean int,
         100k_plus_Male_boolean int,
         0_10k_Female_boolean int,
         10k_25k_Female_boolean int,
         25k_40k_Female_boolean int,
         40k_65k_Female_boolean int,
         65k_100k_Female_boolean int,
         100k_plus_Female_boolean int)"""

cursor.execute(sql)

# 关闭数据库连接
db.close()

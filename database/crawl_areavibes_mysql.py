# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 14:30:20 2016

@author: Junxiao
"""

from bs4 import BeautifulSoup
import urllib2
import re
#import time
from decimal import Decimal
from re import sub
import MySQLdb
#import random
from flask import Flask
app = Flask(__name__)


#%% ZIP information

# 打开数据库连接
db = MySQLdb.connect("localhost","root","123456789o","MMT" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

sql = "SELECT GEOID FROM zip2gps"
cursor.execute(sql)
zip_list_all = map(int, re.findall(r'\d+\.*\d*', str(cursor.fetchall())))
zip_list = [77036]

#zip_list = [77204]

# SQL 查询语句
#zip = 705
for zip in zip_list:
    sql = "SELECT * FROM zip2gps \
           WHERE geoid = '%d'" % (zip)
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
       for row in results:
          GEOID = row[0]
          INTPTLAT = row[1]
          INTPTLONG = row[2]
          # 打印结果
    #      print "GEOID=%d,INTPTLAT=%f,INTPTLONG=%f" % \
    #             (GEOID, INTPTLAT, INTPTLONG )
            
    except:
       print "Error: unable to fecth zip data"   
    
    
    # 找到ZIP CODE的link
    # 两个不同的link供测试
    url = "http://www.areavibes.com/search-results/?zip=%d&ll=%f+%f" % (GEOID, INTPTLAT, INTPTLONG )
#    print 'Process zip = %s' % url
    
    #%% 搜索页
    #print 'wait 3 sec'
    # time.sleep(random.randint(1, 10))
    
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    search_result = soup.findAll(href = re.compile("ll="))
    for link in search_result:
        livability_url= 'http://www.areavibes.com'+ link.get('href')
    
    try:    
        #%% Livability page
        #print 'wait 2 sec'
        # time.sleep(random.randint(1, 10))
        
        livability_page = urllib2.urlopen(livability_url)
        livability_soup = BeautifulSoup(livability_page, 'lxml')
        cost_of_living_url = 'http://www.areavibes.com' + livability_soup.find(href = re.compile("cost-of-living/")).get('href')
        crime_url = 'http://www.areavibes.com' + livability_soup.find(href = re.compile("crime/")).get('href')
        education_url = 'http://www.areavibes.com' + livability_soup.find(href = re.compile("education/")).get('href')
        employment_url = 'http://www.areavibes.com' + livability_soup.find(href = re.compile("employment/")).get('href')
        housing_url = 'http://www.areavibes.com' + livability_soup.find(href = re.compile("housing/")).get('href')
        weather_url = 'http://www.areavibes.com' + livability_soup.find(href = re.compile("weather/")).get('href')
        demographics_url = 'http://www.areavibes.com' + livability_soup.find(href = re.compile("demographics/")).get('href')
        
        table_content = livability_soup.findAll(attrs = {'class':['score-map']})
        livability = map(float, re.findall(r'\d+\.*\d*', str(table_content)))[0]

        
        #%% Cost of living page
        #print 'wait 2 sec'
        # time.sleep(random.randint(1, 10))
        cost_of_living_page = urllib2.urlopen(cost_of_living_url)
        cost_of_living_soup = BeautifulSoup(cost_of_living_page, 'lxml')
        table_content = cost_of_living_soup.findAll(attrs = {'class':['table-overflow-container']})
        
        
        FeatureName = ['Household', 'Owners', 'Renters', 'General Sales Tax', 'With Max Surtax', 
                       'Income Tax (Low)', 'Income Tax (High)', 'Haircut', 'Beauty Salon', 
                       'Toothpaste', 'Shampoo', 'Movie', 'Bowling', 'Ground Beef', 'Fried Chicken', 
                       'Milk', 'Potatoes', 'Pizza', 'Beer', 'Optometrist', 'Doctor','Dentist', 
                       'Ibuprofen', 'Lipitor', 'Home Price', 'Avg. Mortgage Payment', 'Apartment Rent', 
                       'Gasoline', 'Tire Balancing', 'All Electricity', 'Phone']
        offset_cost_of_living = [2, 2, 2, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        boolean_cost_of_living = [0] * (len(FeatureName))
        values_cost_of_living = [0.0] * (len(FeatureName))
        
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                temp_value = temp_GST[j + offset_cost_of_living[k]].contents[0]                        
#                                print FeatureName[k],':\t', temp_value
                                boolean_cost_of_living[k] = 1
                                try:
                                    values_cost_of_living[k] = float(Decimal(sub(r'[^\d.]', '', temp_value)))
                                except:
                                    boolean_cost_of_living[k] = 0
                        break
        
        try:
            sql = "INSERT INTO cost_of_living(GEOID, \
                    Household, Owners, Renters, General_Sales_Tax, \
                    With_Max_Surtax, Income_Tax_Low, Income_Tax_High, Haircut, Beauty_Salon, \
                    Toothpaste, Shampoo, Movie, Bowling, Ground_Beef, Fried_Chicken, Milk, \
                    Potatoes, Pizza, Beer, Optometrist, Doctor, Dentist, Ibuprofen, Lipitor, \
                    Home_Price, Avg_Mortgage_Payment, Apartment_Rent, Gasoline, Tire_Balancing, \
                    All_Electricity, Phone,\
                    Household_boolean, Owners_boolean, Renters_boolean, General_Sales_Tax_boolean, \
                    With_Max_Surtax_boolean, Income_Tax_Low_boolean, Income_Tax_High_boolean, Haircut_boolean, Beauty_Salon_boolean, \
                    Toothpaste_boolean, Shampoo_boolean, Movie_boolean, Bowling_boolean, Ground_Beef_boolean, Fried_Chicken_boolean, Milk_boolean, \
                    Potatoes_boolean, Pizza_boolean, Beer_boolean, Optometrist_boolean, Doctor_boolean, Dentist_boolean, Ibuprofen_boolean, Lipitor_boolean, \
                    Home_Price_boolean, Avg_Mortgage_Payment_boolean, Apartment_Rent_boolean, Gasoline_boolean, Tire_Balancing_boolean, \
                    All_Electricity_boolean, Phone_boolean) \
                    VALUES (%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f,  \
                    %f, %f, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,  \
                    %d, %d)" % \
                    (zip, values_cost_of_living[0], values_cost_of_living[1], values_cost_of_living[2], \
                    values_cost_of_living[3], values_cost_of_living[4], values_cost_of_living[5], \
                    values_cost_of_living[6], values_cost_of_living[7], values_cost_of_living[8], \
                    values_cost_of_living[9], values_cost_of_living[10], values_cost_of_living[11], \
                    values_cost_of_living[12], values_cost_of_living[13], values_cost_of_living[14], \
                    values_cost_of_living[15], values_cost_of_living[16], values_cost_of_living[17], \
                    values_cost_of_living[18], values_cost_of_living[19], values_cost_of_living[20], \
                    values_cost_of_living[21], values_cost_of_living[22], values_cost_of_living[23], \
                    values_cost_of_living[24], values_cost_of_living[25], values_cost_of_living[26], \
                    values_cost_of_living[27], values_cost_of_living[28], values_cost_of_living[29], \
                    values_cost_of_living[30], \
                    boolean_cost_of_living[0], boolean_cost_of_living[1], boolean_cost_of_living[2], \
                    boolean_cost_of_living[3], boolean_cost_of_living[4], boolean_cost_of_living[5], \
                    boolean_cost_of_living[6], boolean_cost_of_living[7], boolean_cost_of_living[8], \
                    boolean_cost_of_living[9], boolean_cost_of_living[10], boolean_cost_of_living[11], \
                    boolean_cost_of_living[12], boolean_cost_of_living[13], boolean_cost_of_living[14], \
                    boolean_cost_of_living[15], boolean_cost_of_living[16], boolean_cost_of_living[17], \
                    boolean_cost_of_living[18], boolean_cost_of_living[19], boolean_cost_of_living[20], \
                    boolean_cost_of_living[21], boolean_cost_of_living[22], boolean_cost_of_living[23], \
                    boolean_cost_of_living[24], boolean_cost_of_living[25], boolean_cost_of_living[26], \
                    boolean_cost_of_living[27], boolean_cost_of_living[28], boolean_cost_of_living[29], \
                    boolean_cost_of_living[30])
#        print sql
           # 执行sql语句
            cursor.execute(sql)
           # 提交到数据库执行
            db.commit()
        except:
           # Rollback in case there is any error
#           print '1'
            db.rollback()        
        
        #%% Crime page
        #print 'wait 2 sec'
        # time.sleep(random.randint(1, 10))
        crime_page = urllib2.urlopen(crime_url)
        crime_soup = BeautifulSoup(crime_page, 'lxml')
        table_content = crime_soup.findAll(attrs = {'class':['table-overflow-container']})
        
        
        FeatureName = ['Murder', 'Rape', 'Robbery', 'Assault', 'Violent crime', 'Burglary', 'Theft', 
                       'Vehicle theft', 'Property crime','Law enforcement employees', 'Police officers']
        offset_crime = [2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1]
        boolean_crime = [0] * (len(FeatureName))
        values_crime = [0.0] * (len(FeatureName))
        
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                temp_value = temp_GST[j + offset_crime[k]].contents[0]                        
#                                print FeatureName[k],':\t', temp_value
                                boolean_crime[k] = 1
                                try:
                                    values_crime[k] = float(Decimal(sub(r'[^\d.]', '', temp_value)))  # deal with n/a
                                except:
                                    boolean_crime[k] = 0
                        break
                    
        # find data of previous year  from figure
        figure_content = crime_soup.findAll(attrs = {'type':['text/javascript']})
        for yy in figure_content:
            yy_str = yy.string
            try:    
                if 'yy_crime' in yy_str:
                    temp_value = map(float, re.findall(r'\d+\.*\d*', str(yy_str)))
                    values_crime = values_crime + temp_value[-3:]
                    boolean_crime = boolean_crime + [1, 1, 1]
#                    print 'Violent (1 years ago):\t', values_crime[k+1]
#                    print 'Property  (1 years ago):\t', values_crime[k+2]
#                    print 'Crime  (1 years ago):\t', values_crime[k+3]
                    break
            except:
                temp_value = [0]
                
        if (len(boolean_crime) == 11):
            values_crime = values_crime + [0.0, 0.0, 0.0]
            boolean_crime = boolean_crime + [0, 0, 0]
                    
        try:
            sql = "INSERT INTO crime(GEOID, Murder, Rape, Robbery, Assault, \
                    Violent_crime, Burglary, Theft, Vehicle_theft, Property_crime, \
                    Law_enforcement_employees, Police_officers, \
                    Violent_1_years_ago, Property_1_years_ago, Crime_1_years_ago, \
                    Murder_boolean, Rape_boolean, Robbery_boolean, Assault_boolean, \
                    Violent_crime_boolean, Burglary_boolean, Theft_boolean, Vehicle_theft_boolean, Property_crime_boolean, \
                    Law_enforcement_employees_boolean, Police_officers_boolean, \
                    Violent_1_years_ago_boolean, Property_1_years_ago_boolean, Crime_1_years_ago_boolean) \
                    VALUES (%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d)" % \
                    (zip, values_crime[0], values_crime[1], values_crime[2], \
                    values_crime[3], values_crime[4], values_crime[5], \
                    values_crime[6], values_crime[7], values_crime[8], \
                    values_crime[9], values_crime[10], values_crime[11], \
                    values_crime[12], values_crime[13], \
                    boolean_crime[0], boolean_crime[1], boolean_crime[2], \
                    boolean_crime[3], boolean_crime[4], boolean_crime[5], \
                    boolean_crime[6], boolean_crime[7], boolean_crime[8], \
                    boolean_crime[9], boolean_crime[10], boolean_crime[11], \
                    boolean_crime[12], boolean_crime[13])
#        print sql
           # 执行sql语句
            cursor.execute(sql)
           # 提交到数据库执行
            db.commit()
        except:
           # Rollback in case there is any error
#           print '1'
            db.rollback()          
        
        
        #%% Education page
        
        #print 'wait 2 sec'
        # time.sleep(random.randint(1, 10))
        education_page = urllib2.urlopen(education_url)
        education_soup = BeautifulSoup(education_page, 'lxml')
        table_content = education_soup.findAll(attrs = {'class':['table-overflow-container']})
        
        FeatureName = ['Average Test Scores', 'Student/Teacher ratio', 'Total public schools',
                       'Total private schools', 'Total post-secondary schools', 'Completed 8th grade', 
                       'Completed high school', 'Completed some college', 'Completed associate degree',
                       'Completed bachelors', 'Completed masters', 'Completed professional degree', 
                       'Completed doctorate']
        offset_education = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        boolean_education = [0] * (len(FeatureName))
        values_education = [0.0] * (len(FeatureName))
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                temp_value = temp_GST[j + offset_education[k]].contents[0]                        
#                                print FeatureName[k],':\t', temp_value
                                boolean_education[k] = 1
                                try:
                                    values_education[k] = float(Decimal(sub(r'[^\d.]', '', temp_value))) # deal with n/a
                                except:
                                    boolean_education[k] = 0
                        break
        
        
        
        # find data of previous year  from figure
        figure_content = education_soup.findAll(attrs = {'type':['text/javascript']})
        k = len(values_education)
        for yy in figure_content:
            yy_str = yy.string
            try:    
                if 'highest_edu' in yy_str:
                    temp_value = map(float, re.findall(r'\d+\.*\d*', str(yy_str)))
                    values_education = values_education + temp_value
                    boolean_education = boolean_education + [1] * 14
#                    print 'High school diploma (Male):\t', values_education[k+0]
#                    print 'Some college (Male):\t', values_education[k+1]
#                    print 'Associates degree (Male):\t', values_education[k+2]
#                    print 'Professional schooling (Male):\t', values_education[k+3]
#                    print 'Bachelor’s degree (Male):\t', values_education[k+4]
#                    print 'Master’s degree (Male):\t', values_education[k+5]
#                    print 'Doctorate degree (Male):\t', values_education[k+6]
#                    print 'High school diploma (Female):\t', values_education[k+7]
#                    print 'Some college (Female):\t', values_education[k+8]
#                    print 'Associates degree (Female):\t', values_education[k+9]
#                    print 'Professional schooling (Female):\t', values_education[k+10]
#                    print 'Bachelor’s degree (Female):\t', values_education[k+11]
#                    print 'Master’s degree (Female):\t', values_education[k+12]
#                    print 'Doctorate degree (Female):\t', values_education[k+13]
                    break
            except:
                temp_value = [0]
                
        if (len(boolean_education) == 13):
            values_education = values_education + [0] * 14
            boolean_education = boolean_education + [0] * 14
            
            
        try:
            sql = "INSERT INTO education(GEOID, \
                    Average_Test_Scores, Student_Teacher_ratio, \
                    Total_public_schools, Total_private_schools, Total_post_secondary_schools, \
                    Completed_8th_grade, Completed_high_school, Completed_some_college, \
                    Completed_associate_degree, Completed_bachelors, Completed_masters, \
                    Completed_professional_degree, Completed_doctorate, High_school_diploma_Male, \
                    Some_college_Male, Associates_degree_Male, Professional_schooling_Male, \
                    Bachelors_degree_Male, Masters_degree_Male, Doctorate_degree_Male, \
                    High_school_diploma_Female, Some_college_Female, Associates_degree_Female, \
                    Professional_schooling_Female, Bachelors_degree_Female, Masters_degree_Female, \
                    Doctorate_degree_Female, \
                    Average_Test_Scores_boolean, Student_Teacher_ratio_boolean, \
                    Total_public_schools_boolean, Total_private_schools_boolean, Total_post_secondary_schools_boolean, \
                    Completed_8th_grade_boolean, Completed_high_school_boolean, Completed_some_college_boolean, \
                    Completed_associate_degree_boolean, Completed_bachelors_boolean, Completed_masters_boolean, \
                    Completed_professional_degree_boolean, Completed_doctorate_boolean, High_school_diploma_Male_boolean, \
                    Some_college_Male_boolean, Associates_degree_Male_boolean, Professional_schooling_Male_boolean, \
                    Bachelors_degree_Male_boolean, Masters_degree_Male_boolean, Doctorate_degree_Male_boolean, \
                    High_school_diploma_Female_boolean, Some_college_Female_boolean, Associates_degree_Female_boolean, \
                    Professional_schooling_Female_boolean, Bachelors_degree_Female_boolean, Masters_degree_Female_boolean, \
                    Doctorate_degree_Female_boolean) \
                    VALUES (%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)" % \
                    (zip, values_education[0], values_education[1], values_education[2], \
                    values_education[3], values_education[4], values_education[5], \
                    values_education[6], values_education[7], values_education[8], \
                    values_education[9], values_education[10], values_education[11], \
                    values_education[12], values_education[13],values_education[14], \
                    values_education[15], values_education[16], values_education[17], \
                    values_education[18], values_education[19], values_education[20], \
                    values_education[21], values_education[22], values_education[23], \
                    values_education[24], values_education[25], values_education[26], \
                    boolean_education[0], boolean_education[1], boolean_education[2], \
                    boolean_education[3], boolean_education[4], boolean_education[5], \
                    boolean_education[6], boolean_education[7], boolean_education[8], \
                    boolean_education[9], boolean_education[10], boolean_education[11], \
                    boolean_education[12], boolean_education[13],boolean_education[14], \
                    boolean_education[15], boolean_education[16], boolean_education[17], \
                    boolean_education[18], boolean_education[19], boolean_education[20], \
                    boolean_education[21], boolean_education[22], boolean_education[23], \
                    boolean_education[24], boolean_education[25], boolean_education[26]) 
    #        print sql
           # 执行sql语句
            cursor.execute(sql)
           # 提交到数据库执行
            db.commit()
        except:
           # Rollback in case there is any error
#           print '1'
            db.rollback()               
            
        #%% Employment page
        
        #print 'wait 2 sec'
        # time.sleep(random.randint(1, 10))
        employment_page = urllib2.urlopen(employment_url)
        employment_soup = BeautifulSoup(employment_page, 'lxml')
        table_content = employment_soup.findAll(attrs = {'class':['table-overflow-container']})    
        
        
        
        FeatureName = ['Income per capita', 'Median household income', 'Median income owner occupied',
                       'Median income renter occupied', 'Median earnings male', 'Median earnings female', 
                       'Unemployment rate', 'Poverty level']
        offset_employment = [1, 1, 1, 1, 1, 1, 1, 1]
        boolean_employment = [0] * (len(FeatureName))
        values_employment = [0.0] * (len(FeatureName))
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                temp_value = temp_GST[j + offset_employment[k]].contents[0]                        
#                                print FeatureName[k],':\t', temp_value
                                boolean_employment[k] = 1
                                try:
                                    values_employment[k] = float(Decimal(sub(r'[^\d.]', '', temp_value))) # deal with n/a
                                except:
                                    boolean_employment[k] = 0
                        break
        
        FeatureName = ['Construction industry', 'Manufacturing sector', 'Financial & insurance services',
                       'Wholesale & retail services', 'Public administration', 
                       'Transportation, warehousing & utilities', 'Education, health & social services', 'Other']
        offset_employment = [1, 1, 1, 1, 1, 1, 1, 1]
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                try:
                                    temp_value = temp_GST[j + offset_employment[k]].contents[0]                        
#                                    print FeatureName[k],'(Male):\t', temp_value
                                    boolean_employment = boolean_employment + [1]
                                    values_employment = values_employment + [float(Decimal(sub(r'[^\d.]', '', temp_value)))] # deal with n/a
                                except:
                                    boolean_employment = boolean_employment + [0]
                                    values_employment = values_employment + [0]
                        break
        
        offset_employment = [2, 2, 2, 2, 2, 2, 2, 2]
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                try:
                                    temp_value = temp_GST[j + offset_employment[k]].contents[0]                        
#                                    print FeatureName[k],'(Female):\t', temp_value
                                    boolean_employment = boolean_employment + [1]
                                    values_employment = values_employment + [float(Decimal(sub(r'[^\d.]', '', temp_value)))] # deal with n/a
                                except:
                                    boolean_employment = boolean_employment + [0]
                                    values_employment = values_employment + [0]
                        break     
        
        
        # find data of previous year  from figure
        figure_content = employment_soup.findAll(attrs = {'type':['text/javascript']})
        k = len(values_employment)
        for yy in figure_content:
            yy_str = str(yy.string)
            try:    
                if 'work_type' in yy_str:
                    yy_str = yy_str.replace('35 hours', '')
                    yy_str = yy_str.replace('34 to 15', '')
                    yy_str = yy_str.replace('14 to 1', '')
                    temp_value = map(float, re.findall(r'\d+\.*\d*', yy_str))
                    values_employment = values_employment + temp_value
                    boolean_employment = boolean_employment + [1] * 12
#                    print 'In labor force:\t', values_employment[k+0]
#                    print 'Military:\t', values_employment[k+1]
#                    print 'Unemployed:\t', values_employment[k+2]
#                    print 'Unknown/Other:\t', values_employment[k+3]
#                    print '35 hours plus (Male):\t', values_employment[k+4]
#                    print '34 to 15 hours (Male):\t', values_employment[k+5]
#                    print '14 to 1 hours (Male):\t', values_employment[k+6]
#                    print 'None (Male):\t', values_employment[k+7]
#                    print '35 hours plus (Female):\t', values_employment[k+8]
#                    print '34 to 15 hours (Female):\t', values_employment[k+9]
#                    print '14 to 1 hours (Male):\t', values_employment[k+10]
#                    print 'None (Female):\t', values_employment[k+11]
                    break
            except:
                temp_value = [0]
                
        if (len(boolean_employment) == 24):
            values_employment = values_employment + [0] * 12
            boolean_employment = boolean_employment + [0] * 12   
        
        
        
        k = len(values_employment)
        for yy in figure_content:
            yy_str = str(yy.string)
            try:    
                if 'wage_brackets' in yy_str:
        #            print yy_str
                    yy_str = yy_str.replace('$0 - 10K', '')
                    yy_str = yy_str.replace('$10K - 25K', '')
                    yy_str = yy_str.replace('$25K - 40K', '')
                    yy_str = yy_str.replace('$40K - 65K', '')
                    yy_str = yy_str.replace('$65K - 100K', '')
                    yy_str = yy_str.replace('$100K plus', '')
                    temp_value = map(float, re.findall(r'\d+\.*\d*', yy_str))
        #            print temp_value
                    values_employment = values_employment + temp_value
                    boolean_employment = boolean_employment + [1] * 12
#                    print '0 - 10k (Male):\t', values_employment[k+0]
#                    print '10k - 25k (Male):\t', values_employment[k+1]
#                    print '25k - 40k (Male):\t', values_employment[k+2]
#                    print '40k - 65k (Male):\t', values_employment[k+3]
#                    print '65k - 100k (Male):\t', values_employment[k+4]
#                    print '100k plus (Male):\t', values_employment[k+5]
#                    print '0 - 10k (Female):\t', values_employment[k+6]
#                    print '10k - 25k (Female):\t', values_employment[k+7]
#                    print '25k - 40k (Female):\t', values_employment[k+8]
#                    print '40k - 65k (Female):\t', values_employment[k+9]
#                    print '65k - 100k (Female):\t', values_employment[k+10]
#                    print '100k plus (Female):\t', values_employment[k+11]
                    break
            except:
                temp_value = [0]
                
        if (len(boolean_employment) == 36):
            values_employment = values_employment + [0] * 12
            boolean_employment = boolean_employment + [0] * 12   
        

        try:
            sql = "INSERT INTO employment(GEOID, Income_per_capita, Median_household_income, \
                    Median_income_owner_occupied, Median_income_renter_occupied, \
                    Median_earnings_male, Median_earnings_female, Unemployment_rate, \
                    Poverty_level, Construction_industry_Male, Manufacturing_sector_Male, \
                    Financial_insurance_services_Male, Wholesale_retail_services_Male, \
                    Public_administration_Male, Transportation_warehousing_utilities_Male, \
                    Education_health_social_services_Male, Other_employment_Male, \
                    Construction_industry_Female, Manufacturing_sector_Female, \
                    Financial_insurance_services_Female, Wholesale_retail_services_Female, \
                    Public_administration_Female, Transportation_warehousing_utilities_Female, \
                    Education_health_social_services_Female, Other_employment_Female, \
                    In_labor_force, Military, Unemployed, Unknown_Other, \
                    35_hours_plus_Male, 34_to_15_hours_Male, 14_to_1_hours_Male, None_Male, \
                    35_hours_plus_Female, 34_to_15_hours_Female, 14_to_1_hours_Female, None_Female, \
                    0_10k_Male, 10k_25k_Male, 25k_40k_Male, 40k_65k_Male, 65k_100k_Male, 100k_plus_Male, \
                    0_10k_Female, 10k_25k_Female, 25k_40k_Female, 40k_65k_Female, \
                    65k_100k_Female, 100k_plus_Female, \
                    Income_per_capita_boolean, Median_household_income_boolean, \
                    Median_income_owner_occupied_boolean, Median_income_renter_occupied_boolean, \
                    Median_earnings_male_boolean, Median_earnings_female_boolean, Unemployment_rate_boolean, \
                    Poverty_level_boolean, Construction_industry_Male_boolean, Manufacturing_sector_Male_boolean, \
                    Financial_insurance_services_Male_boolean, Wholesale_retail_services_Male_boolean, \
                    Public_administration_Male_boolean, Transportation_warehousing_utilities_Male_boolean, \
                    Education_health_social_services_Male_boolean, Other_employment_Male_boolean, \
                    Construction_industry_Female_boolean, Manufacturing_sector_Female_boolean, \
                    Financial_insurance_services_Female_boolean, Wholesale_retail_services_Female_boolean, \
                    Public_administration_Female_boolean, Transportation_warehousing_utilities_Female_boolean, \
                    Education_health_social_services_Female_boolean, Other_employment_Female_boolean, \
                    In_labor_force_boolean, Military_boolean, Unemployed_boolean, Unknown_Other_boolean, \
                    35_hours_plus_Male_boolean, 34_to_15_hours_Male_boolean, 14_to_1_hours_Male_boolean, None_Male_boolean, \
                    35_hours_plus_Female_boolean, 34_to_15_hours_Female_boolean, 14_to_1_hours_Female_boolean, None_Female_boolean, \
                    0_10k_Male_boolean, 10k_25k_Male_boolean, 25k_40k_Male_boolean, 40k_65k_Male_boolean, 65k_100k_Male_boolean, 100k_plus_Male_boolean, \
                    0_10k_Female_boolean, 10k_25k_Female_boolean, 25k_40k_Female_boolean, 40k_65k_Female_boolean, \
                    65k_100k_Female_boolean, 100k_plus_Female_boolean) \
                    VALUES (%d, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d)" % \
                    (zip, values_employment[0], values_employment[1], values_employment[2], \
                    values_employment[3], values_employment[4], values_employment[5], \
                    values_employment[6], values_employment[7], values_employment[8], \
                    values_employment[9], values_employment[10], values_employment[11], \
                    values_employment[12], values_employment[13],values_employment[14], \
                    values_employment[15], values_employment[16], values_employment[17], \
                    values_employment[18], values_employment[19], values_employment[20], \
                    values_employment[21], values_employment[22], values_employment[23], \
                    values_employment[24], values_employment[25], values_employment[26], \
                    values_employment[27], values_employment[28], values_employment[29], \
                    values_employment[30], values_employment[31], values_employment[32], \
                    values_employment[33], values_employment[34], values_employment[35], \
                    values_employment[36], values_employment[37], values_employment[38], \
                    values_employment[39], values_employment[40],values_employment[41], \
                    values_employment[42], values_employment[43], values_employment[44], \
                    values_employment[45], values_employment[46], values_employment[47], \
                    boolean_employment[0], boolean_employment[1], boolean_employment[2], \
                    boolean_employment[3], boolean_employment[4], boolean_employment[5], \
                    boolean_employment[6], boolean_employment[7], boolean_employment[8], \
                    boolean_employment[9], boolean_employment[10], boolean_employment[11], \
                    boolean_employment[12], boolean_employment[13],boolean_employment[14], \
                    boolean_employment[15], boolean_employment[16], boolean_employment[17], \
                    boolean_employment[18], boolean_employment[19], boolean_employment[20], \
                    boolean_employment[21], boolean_employment[22], boolean_employment[23], \
                    boolean_employment[24], boolean_employment[25], boolean_employment[26], \
                    boolean_employment[27], boolean_employment[28], boolean_employment[29], \
                    boolean_employment[30], boolean_employment[31], boolean_employment[32], \
                    boolean_employment[33], boolean_employment[34], boolean_employment[35], \
                    boolean_employment[36], boolean_employment[37], boolean_employment[38], \
                    boolean_employment[39], boolean_employment[40],boolean_employment[41], \
                    boolean_employment[42], boolean_employment[43], boolean_employment[44], \
                    boolean_employment[45], boolean_employment[46], boolean_employment[47]) 
    #        print sql
           # 执行sql语句
            cursor.execute(sql)
           # 提交到数据库执行
            db.commit()
        except:
           # Rollback in case there is any error
#           print '1'
            db.rollback()         
        
        
        #%% Housing page
        
        #print 'wait 2 sec'
        # time.sleep(random.randint(1, 10))
        housing_page = urllib2.urlopen(housing_url)
        housing_soup = BeautifulSoup(housing_page, 'lxml')
        table_content = housing_soup.findAll(attrs = {'class':['table-overflow-container']})    
        
        FeatureName = ['Median home price', 'Median rent asked', 'Avg. people per household',
                       'Owner occupied households', 'Renter occupied households']
        offset_housing = [1, 1, 1, 1, 1]
        boolean_housing = [0] * (len(FeatureName))
        values_housing = [0.0] * (len(FeatureName))
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                temp_value = temp_GST[j + offset_housing[k]].contents[0]
#                                print FeatureName[k],':\t', temp_value
                                boolean_housing[k] = 1
                                try:
                                    values_housing[k] = float(Decimal(sub(r'[^\d.]', '', temp_value))) # deal with n/a
                                except:
                                    boolean_housing[k] = 0
                        break
        
        # find data of previous year  from figure
        figure_content = housing_soup.findAll(attrs = {'type':['text/javascript']})
        k = len(values_housing)
        for yy in figure_content:
            yy_str = str(yy.string)
            try:    
                if 'vac_occ_lvls' in yy_str:
        #            print yy_str
                    yy_str = yy_str.replace('0-9%', '')
                    yy_str = yy_str.replace('10-19%', '')
                    yy_str = yy_str.replace('20-29%', '')
                    yy_str = yy_str.replace('30-39%', '')
                    yy_str = yy_str.replace('40-49%', '')
                    yy_str = yy_str.replace('50%+', '')
                    temp_value = map(float, re.findall(r'\d+\.*\d*', yy_str))
                    values_housing = values_housing + temp_value
        #            print temp_value
                    boolean_housing = boolean_housing + [1] * 27
#                    print 'Occupied:\t', values_housing[k+0]
#                    print 'Vacant:\t', values_housing[k+1]
#                    print 'For rent:\t', values_housing[k+2]
#                    print 'For sale only:\t', values_housing[k+3]
#                    print 'Rented\Sold not occ:\t', values_housing[k+4]
#                    print 'Seasonal:\t', values_housing[k+5]
#                    print 'Migrant workers:\t', values_housing[k+6]
#                    print 'Other:\t', values_housing[k+7]
#                    print 'Avg. household size:\t', values_housing[k+8]
#                    print 'Avg. household size owner occ:\t', values_housing[k+9]
#                    print 'Avg. household size renter occ:\t', values_housing[k+10]
#                    print 'Median house-hold rooms:\t', values_housing[k+11]
#                    print 'Utility gas:\t', values_housing[k+12]
#                    print 'Electricity:\t', values_housing[k+13]
#                    print 'Oil or kerosene:\t', values_housing[k+14]
#                    print 'Solar:\t', values_housing[k+15]
#                    print 'Other:\t', values_housing[k+16]
#                    print 'None:\t', values_housing[k+17]
#                    print '0-9%:\t', values_housing[k+18]
#                    print '10-19%:\t', values_housing[k+19]
#                    print '20-29%:\t', values_housing[k+20]
#                    print '30-39%:\t', values_housing[k+21]
#                    print '40-49%:\t', values_housing[k+22]
#                    print '50%+:\t', values_housing[k+23]
#                    print 'N/A:\t', values_housing[k+24]
#                    print 'Utilities extra:\t', values_housing[k+25]
#                    print 'Utilities included:\t', values_housing[k+26]
                    break
            except:
                temp_value = [0]
                
        if (len(boolean_housing) == 5):
            values_housing = values_housing + [0.0] * 27
            boolean_housing = boolean_housing + [0] * 27   
        


        try:
            sql = "INSERT INTO housing(GEOID, Median_home_price, Median_rent_asked, \
                    Avg_people_per_household, Owner_occupied_households, \
                    Renter_occupied_households, Occupied, Vacant, \
                    For_rent, For_sale_only, Rented_Sold_not_occ, \
                    Seasonal, Migrant_workers, \
                    Other_occ, Avg_household_size, \
                    Avg_household_size_owner_occ, Avg_household_size_renter_occ, \
                    Median_house_hold_rooms, Utility_gas, \
                    Electricity, Oil_or_kerosene, \
                    Solar, Other_heat, \
                    None_heat, 0_9per, \
                    10_19per, 20_29per, 30_39per, 40_49per, \
                    50per_plus, N_A, Utilities_extra, Utilities_included, \
                    Median_home_price_boolean, Median_rent_asked_boolean, \
                    Avg_people_per_household_boolean, Owner_occupied_households_boolean, \
                    Renter_occupied_households_boolean, Occupied_boolean, Vacant_boolean, \
                    For_rent_boolean, For_sale_only_boolean, Rented_Sold_not_occ_boolean, \
                    Seasonal_boolean, Migrant_workers_boolean, \
                    Other_occ_boolean, Avg_household_size_boolean, \
                    Avg_household_size_owner_occ_boolean, Avg_household_size_renter_occ_boolean, \
                    Median_house_hold_rooms_boolean, Utility_gas_boolean, \
                    Electricity_boolean, Oil_or_kerosene_boolean, \
                    Solar_boolean, Other_heat_boolean, \
                    None_heat_boolean, 0_9per_boolean, \
                    10_19per_boolean, 20_29per_boolean, 30_39per_boolean, 40_49per_boolean, \
                    50per_plus_boolean, N_A_boolean, Utilities_extra_boolean, Utilities_included_boolean) \
                    VALUES (%d, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d)" % \
                    (zip, values_housing[0], values_housing[1], values_housing[2], \
                    values_housing[3], values_housing[4], values_housing[5], \
                    values_housing[6], values_housing[7], values_housing[8], \
                    values_housing[9], values_housing[10], values_housing[11], \
                    values_housing[12], values_housing[13],values_housing[14], \
                    values_housing[15], values_housing[16], values_housing[17], \
                    values_housing[18], values_housing[19], values_housing[20], \
                    values_housing[21], values_housing[22], values_housing[23], \
                    values_housing[24], values_housing[25], values_housing[26], \
                    values_housing[27], values_housing[28], values_housing[29], \
                    values_housing[30], values_housing[31],
                    boolean_housing[0], boolean_housing[1], boolean_housing[2], \
                    boolean_housing[3], boolean_housing[4], boolean_housing[5], \
                    boolean_housing[6], boolean_housing[7], boolean_housing[8], \
                    boolean_housing[9], boolean_housing[10], boolean_housing[11], \
                    boolean_housing[12], boolean_housing[13],boolean_housing[14], \
                    boolean_housing[15], boolean_housing[16], boolean_housing[17], \
                    boolean_housing[18], boolean_housing[19], boolean_housing[20], \
                    boolean_housing[21], boolean_housing[22], boolean_housing[23], \
                    boolean_housing[24], boolean_housing[25], boolean_housing[26], \
                    boolean_housing[27], boolean_housing[28], boolean_housing[29], \
                    boolean_housing[30], boolean_housing[31]) 
    #        print sql
           # 执行sql语句
            cursor.execute(sql)
           # 提交到数据库执行
            db.commit()
        except:
           # Rollback in case there is any error
#           print '1'
            db.rollback()   
            
            
        #%% weather page
        
        #print 'wait 2 sec'
        # time.sleep(random.randint(1, 10))
        weather_page = urllib2.urlopen(weather_url)
        weather_soup = BeautifulSoup(weather_page, 'lxml')
        table_content = weather_soup.findAll(attrs = {'class':['table-overflow-container']})            
        
        
        FeatureName = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                       'September', 'October', 'November', 'December']
        offset_weather = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 ,1]
        boolean_weather = [0] * (len(FeatureName))
        values_weather = [0.0] * (len(FeatureName))
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                temp_value = temp_GST[j + offset_weather[k]].contents[0]
#                                print FeatureName[k],'(min):\t', temp_value
                                boolean_weather[k] = 1
                                try:
                                    values_weather[k] = float(Decimal(sub(r'[^\d.]', '', temp_value))) # deal with n/a
                                except:
                                    boolean_weather[k] = 0
                        break
        
        offset_weather = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ,2 ,2]
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                try:
                                    temp_value = temp_GST[j + offset_weather[k]].contents[0]                        
#                                    print FeatureName[k],'(max):\t', temp_value
                                    boolean_weather = boolean_weather + [1]
                                    values_weather = values_weather + [float(Decimal(sub(r'[^\d.]', '', temp_value)))] # deal with n/a
                                except:
                                    boolean_weather = boolean_weather + [0]
                                    values_weather = values_weather + [0.0]
                        break
        
        
        offset_weather = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ,3 ,3]
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                try:
                                    temp_value = temp_GST[j + offset_weather[k]].contents[0]                        
#                                    print FeatureName[k],'(avg):\t', temp_value
                                    boolean_weather = boolean_weather + [1]
                                    values_weather = values_weather + [float(Decimal(sub(r'[^\d.]', '', temp_value)))] # deal with n/a
                                except:
                                    boolean_weather = boolean_weather + [0]
                                    values_weather = values_weather + [0.0]
                        break
                    
        FeatureName = ['Air quality index', 'Pollution index', 'Days measured', 'Days with good air quality',
                       'Days with moderate air quality', 'Days w/ poor A.Q. for sensitive groups',
                       'Days with unhealthy air quality', 'Arsenic', 'Benzene', 'Carbon Tetrachloride',
                       'Lead', 'Mercury']
        offset_weather = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 ,1]
        
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:
                            if temp_GST[j].string == FeatureName[k]:
                                try:
                                    temp_value = temp_GST[j + offset_weather[k]].contents[0]                        
#                                    print FeatureName[k],':\t', temp_value
                                    boolean_weather = boolean_weather + [1]
                                    values_weather = values_weather + [float(Decimal(sub(r'[^\d.]', '', temp_value)))] # deal with n/a
                                except:
                                    boolean_weather = boolean_weather + [0]
                                    values_weather = values_weather + [0.0]
                        break          
        

        try:
            sql = "INSERT INTO weather(GEOID, January_min, February_min, March_min, April_min, \
                    May_min, June_min, July_min, August_min, September_min, October_min, November_min, \
                    December_min, January_max, February_max, March_max, April_max, May_max, June_max, \
                    July_max, August_max, September_max, October_max, November_max, December_max, \
                    January_avg, February_avg, March_avg, April_avg, May_avg, June_avg, July_avg, \
                    August_avg, September_avg, October_avg, November_avg, December_avg, Air_quality_index, \
                    Pollution_index, Days_measured, Days_with_good_air_quality, Days_with_moderate_air_quality, \
                    Days_w_poor_A_Q_for_sensitive_groups, Days_with_unhealthy_air_quality, \
                    Arsenic, Benzene, Carbon_Tetrachloride, Lead, Mercury, \
                    January_min_boolean, February_min_boolean, March_min_boolean, April_min_boolean, \
                    May_min_boolean, June_min_boolean, July_min_boolean, August_min_boolean, September_min_boolean, October_min_boolean, November_min_boolean, \
                    December_min_boolean, January_max_boolean, February_max_boolean, March_max_boolean, April_max_boolean, May_max_boolean, June_max_boolean, \
                    July_max_boolean, August_max_boolean, September_max_boolean, October_max_boolean, November_max_boolean, December_max_boolean, \
                    January_avg_boolean, February_avg_boolean, March_avg_boolean, April_avg_boolean, May_avg_boolean, June_avg_boolean, July_avg_boolean, \
                    August_avg_boolean, September_avg_boolean, October_avg_boolean, November_avg_boolean, December_avg_boolean, Air_quality_index_boolean, \
                    Pollution_index_boolean, Days_measured_boolean, Days_with_good_air_quality_boolean, Days_with_moderate_air_quality_boolean, \
                    Days_w_poor_A_Q_for_sensitive_groups_boolean, Days_with_unhealthy_air_quality_boolean, \
                    Arsenic_boolean, Benzene_boolean, Carbon_Tetrachloride_boolean, Lead_boolean, Mercury_boolean) \
                    VALUES (%d, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d)" % \
                    (zip, values_weather[0], values_weather[1], values_weather[2], \
                    values_weather[3], values_weather[4], values_weather[5], \
                    values_weather[6], values_weather[7], values_weather[8], \
                    values_weather[9], values_weather[10], values_weather[11], \
                    values_weather[12], values_weather[13],values_weather[14], \
                    values_weather[15], values_weather[16], values_weather[17], \
                    values_weather[18], values_weather[19], values_weather[20], \
                    values_weather[21], values_weather[22], values_weather[23], \
                    values_weather[24], values_weather[25], values_weather[26], \
                    values_weather[27], values_weather[28], values_weather[29], \
                    values_weather[30], values_weather[31], values_weather[32], \
                    values_weather[33], values_weather[34], values_weather[35], \
                    values_weather[36], values_weather[37], values_weather[38], \
                    values_weather[39], values_weather[40], values_weather[41], \
                    values_weather[42], values_weather[43], values_weather[44], \
                    values_weather[45], values_weather[46], values_weather[47], \
                    boolean_weather[0], boolean_weather[1], boolean_weather[2], \
                    boolean_weather[3], boolean_weather[4], boolean_weather[5], \
                    boolean_weather[6], boolean_weather[7], boolean_weather[8], \
                    boolean_weather[9], boolean_weather[10], boolean_weather[11], \
                    boolean_weather[12], boolean_weather[13],boolean_weather[14], \
                    boolean_weather[15], boolean_weather[16], boolean_weather[17], \
                    boolean_weather[18], boolean_weather[19], boolean_weather[20], \
                    boolean_weather[21], boolean_weather[22], boolean_weather[23], \
                    boolean_weather[24], boolean_weather[25], boolean_weather[26], \
                    boolean_weather[27], boolean_weather[28], boolean_weather[29], \
                    boolean_weather[30], boolean_weather[31], boolean_weather[32], \
                    boolean_weather[33], boolean_weather[34], boolean_weather[35], \
                    boolean_weather[36], boolean_weather[37], boolean_weather[38], \
                    boolean_weather[39], boolean_weather[40], boolean_weather[41], \
                    boolean_weather[42], boolean_weather[43], boolean_weather[44], \
                    boolean_weather[45], boolean_weather[46], boolean_weather[47]) 
    #        print sql
           # 执行sql语句
            cursor.execute(sql)
           # 提交到数据库执行
            db.commit()
        except:
           # Rollback in case there is any error
#           print '1'
            db.rollback()  
            
            
            
        #%% Demographics page
        
        #print 'wait 2 sec'
        # time.sleep(random.randint(1, 10))
        demographics_page = urllib2.urlopen(demographics_url)
        demographics_soup = BeautifulSoup(demographics_page, 'lxml')
        table_content = demographics_soup.findAll(attrs = {'class':['table-overflow-container']})
        
        
        
        FeatureName = ['Population', 'Population density', 'Median age', 'Male/Female ratio', 'Married ', 
                       'Caucasian', 'African American', 'Asian', 
                       'American Indian', 'Native Hawaiian', 'Mixed race', 'Other race']
        offset_demographics = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 , 1, 1, 1]
        boolean_demographics = [0] * (len(FeatureName))
        values_demographics = [0.0] * (len(FeatureName))
        
        for i in [n for n in range(0,len(table_content))]:
            for k in [p for p in range(0,len(FeatureName))]:
                for temp_FeatureName in table_content[i].find_all("td"):
                    if temp_FeatureName.string == FeatureName[k]:
                        temp_GST = table_content[i].find_all("td")
                        for j in [m for m in range(0,len(temp_GST))]:  
                            try:
                                temp_GST[j].small.extract()
                            except:
                                temp_value = [0] 
                            if temp_GST[j].string == FeatureName[k]:
                                temp_value = str(temp_GST[j + offset_demographics[k]].contents[0])
                                temp_value = temp_value.replace(':1', '')
#                                print FeatureName[k],':\t', temp_value
                                boolean_demographics[k] = 1
                                try:
                                    values_demographics[k] = float(Decimal(sub(r'[^\d.]', '', temp_value))) # deal with n/a
                                except:
                                    boolean_demographics[k] = 0
                        break
        
        table_content = demographics_soup.findAll(attrs = {'class':['block-explain']})
        try:
            temp_value = map(float, re.findall(r'\d+\.*\d*', str(table_content)))
            values_demographics = values_demographics + temp_value
            boolean_demographics = boolean_demographics + [1]
#            print 'Hispanic or Latino origin: ',temp_value[0],'%'
        except:
            values_demographics = values_demographics + [0.0]
            boolean_demographics = boolean_demographics + [0]
        
        # find data of previous year  from figure
        figure_content = demographics_soup.findAll(attrs = {'type':['text/javascript']})
        k = len(values_demographics)
        for yy in figure_content:
            yy_str = str(yy.string)
            try:    
                if 'lang_split' in yy_str:
        #            print yy_str
                    yy_str = yy_str.replace('$200K plus', '')
                    yy_str = yy_str.replace('$150K-$200K', '')
                    yy_str = yy_str.replace('$100K-$150K', '')
                    yy_str = yy_str.replace('$60K-$100K', '')
                    yy_str = yy_str.replace('$40K-$60K', '')
                    yy_str = yy_str.replace('$25K-$40K', '')            
                    yy_str = yy_str.replace('$10K-$25K', '')
                    yy_str = yy_str.replace('$10K or less', '')
                    yy_str = yy_str.replace('< 5', '')
                    yy_str = yy_str.replace('5-14', '')
                    yy_str = yy_str.replace('15-19', '')
                    yy_str = yy_str.replace('20-24', '')
                    yy_str = yy_str.replace('25-34', '')
                    yy_str = yy_str.replace('35-44', '')
                    yy_str = yy_str.replace('45-54', '')
                    yy_str = yy_str.replace('55-64', '')    
                    yy_str = yy_str.replace('65-84', '') 
                    yy_str = yy_str.replace('84 >', '') 
                    yy_str = yy_str.replace('Younger than 6 only', '') 
                    yy_str = yy_str.replace('Both younger than 6', '') 
                    yy_str = yy_str.replace('between 6 and 17', '')
                    yy_str = yy_str.replace('6 to 17 only', '') 
        #            print yy_str
                    temp_value = map(float, re.findall(r'\d+\.*\d*', yy_str))
        #            print temp_value
                    values_demographics = values_demographics + temp_value
                    boolean_demographics = boolean_demographics + [1] * 56
#                    print 'Speak English:\t', values_demographics[k+0]
#                    print 'Speak Spanish:\t', values_demographics[k+1]
#                    print 'Other:\t', values_demographics[k+2]
#                    print 'In state of res:\t', values_demographics[k+3]
#                    print 'Out of state:\t', values_demographics[k+4]
#                    print 'Out of US:\t', values_demographics[k+5]
#                    print 'Foreign:\t', values_demographics[k+6]
#                    print '$200K plus:\t', values_demographics[k+7]
#                    print '$150K-$200K:\t', values_demographics[k+8]
#                    print '$100K-$150K:\t', values_demographics[k+9]
#                    print '$60K-$100K:\t', values_demographics[k+10]
#                    print '$40K-$60K:\t', values_demographics[k+11]
#                    print '$25K-$40K:\t', values_demographics[k+12]
#                    print '$10K-$25K:\t', values_demographics[k+13]
#                    print '$10K or less:\t', values_demographics[k+14]
#                    print 'Salary:\t', values_demographics[k+15]
#                    print 'Self Emp.:\t', values_demographics[k+16]
#                    print 'Investments:\t', values_demographics[k+17]
#                    print 'Social Sec.:\t', values_demographics[k+18]
#                    print 'Supplmental Sec.:\t', values_demographics[k+19]
#                    print 'Public Asst.:\t', values_demographics[k+20]
#                    print 'Retirment Inc.:\t', values_demographics[k+21]
#                    print 'Other:\t', values_demographics[k+22]
#                    print '<5 (Male):\t', values_demographics[k+23]
#                    print '5 - 14 (Male):\t', values_demographics[k+24]
#                    print '15 - 19 (Male):\t', values_demographics[k+25]
#                    print '20 - 24 (Male):\t', values_demographics[k+26]
#                    print '25 - 34 (Male):\t', values_demographics[k+27]
#                    print '35 - 44 (Male):\t', values_demographics[k+28]
#                    print '45 - 54 (Male):\t', values_demographics[k+29]
#                    print '55 - 64 (Male):\t', values_demographics[k+30]
#                    print '65 - 84 (Male):\t', values_demographics[k+31]
#                    print '> 85 (Male):\t', values_demographics[k+32]
#                    print '<5 (Female):\t', values_demographics[k+33]
#                    print '5 - 14 (Female):\t', values_demographics[k+34]
#                    print '15 - 19 (Female):\t', values_demographics[k+35]
#                    print '20 - 24 (Female):\t', values_demographics[k+36]
#                    print '25 - 34 (Female):\t', values_demographics[k+37]
#                    print '35 - 44 (Female):\t', values_demographics[k+38]
#                    print '45 - 54 (Female):\t', values_demographics[k+39]
#                    print '55 - 64 (Female):\t', values_demographics[k+40]
#                    print '65 - 84 (Female):\t', values_demographics[k+41]
#                    print '>85 (Female):\t', values_demographics[k+42]
#                    print 'Never (Male):\t', values_demographics[k+43]
#                    print 'Married (Male):\t', values_demographics[k+44]
#                    print 'Separated (Male):\t', values_demographics[k+45]
#                    print 'Divorced (Male):\t', values_demographics[k+46]
#                    print 'Widowed (Male):\t', values_demographics[k+47]
#                    print 'Never (Female):\t', values_demographics[k+48]
#                    print 'Married (Female):\t', values_demographics[k+49]
#                    print 'Separated (Female):\t', values_demographics[k+50]
#                    print 'Divorced (Female):\t', values_demographics[k+51]
#                    print 'Widowed (Female):\t', values_demographics[k+52]
#                    print 'Younger than 6 only:\t', values_demographics[k+53]
#                    print 'Both younger than 6 & between 6 and 17:\t', values_demographics[k+54]
#                    print '6 to 17 only:\t', values_demographics[k+55]
                    break
            except:
                temp_value = [0]
                
        if (len(boolean_demographics) == 15):
            values_demographics = values_demographics + [0.0] * 56
            boolean_demographics = boolean_demographics + [0] * 56   


        try:
            sql = "INSERT INTO demographics(GEOID, Population, Population_density, Median_age, \
                    Male_Female_ratio, Married, Caucasian, African_American, Asian, \
                    American_Indian, Native_Hawaiian, Mixed_race, Other_race, Hispanic_or_Latino_origin, \
                    Speak_English, Speak_Spanish, Other_language, In_state_of_res_BORN, Out_of_state_BORN, \
                    Out_of_US_BORN, Foreign_BORN, USD200K_plus, USD150K_USD200K, USD100K_USD150K, \
                    USD60K_USD100K, USD40K_USD60K, USD25K_USD40K, USD10K_USD25K, USD10K_or_less, \
                    Salary, Self_Emp, Investments, Social_Sec, Supplmental_Sec, Public_Asst, \
                    Retirment_Inc, Other_income, LESS5_Male, 5_14_Male, 15_19_Male, 20_24_Male, \
                    25_34_Male, 35_44_Male, 45_54_Male, 55_64_Male, 65_84_Male, GREATER85_Male, \
                    LESS5_Female, 5_14_Female, 15_19_Female, 20_24_Female, 25_34_Female, 35_44_Female, \
                    45_54_Female, 55_64_Female, 65_84_Female, GREATER85_Female, Never_Male, \
                    Married_Male, Separated_Male, Divorced_Male, Widowed_Male, Never_Female, \
                    Married_Female, Separated_Female, Divorced_Female, Widowed_Female, \
                    Younger_than_6_only, Both_younger_than_6_between_6_and_17, 6_to_17_only, \
                    Population_boolean, Population_density_boolean, Median_age_boolean, \
                    Male_Female_ratio_boolean, Married_boolean, Caucasian_boolean, African_American_boolean, Asian_boolean, \
                    American_Indian_boolean, Native_Hawaiian_boolean, Mixed_race_boolean, Other_race_boolean, Hispanic_or_Latino_origin_boolean, \
                    Speak_English_boolean, Speak_Spanish_boolean, Other_language_boolean, In_state_of_res_BORN_boolean, Out_of_state_BORN_boolean, \
                    Out_of_US_BORN_boolean, Foreign_BORN_boolean, USD200K_plus_boolean, USD150K_USD200K_boolean, USD100K_USD150K_boolean, \
                    USD60K_USD100K_boolean, USD40K_USD60K_boolean, USD25K_USD40K_boolean, USD10K_USD25K_boolean, USD10K_or_less_boolean, \
                    Salary_boolean, Self_Emp_boolean, Investments_boolean, Social_Sec_boolean, Supplmental_Sec_boolean, Public_Asst_boolean, \
                    Retirment_Inc_boolean, Other_income_boolean, LESS5_Male_boolean, 5_14_Male_boolean, 15_19_Male_boolean, 20_24_Male_boolean, \
                    25_34_Male_boolean, 35_44_Male_boolean, 45_54_Male_boolean, 55_64_Male_boolean, 65_84_Male_boolean, GREATER85_Male_boolean, \
                    LESS5_Female_boolean, 5_14_Female_boolean, 15_19_Female_boolean, 20_24_Female_boolean, 25_34_Female_boolean, 35_44_Female_boolean, \
                    45_54_Female_boolean, 55_64_Female_boolean, 65_84_Female_boolean, GREATER85_Female_boolean, Never_Male_boolean, \
                    Married_Male_boolean, Separated_Male_boolean, Divorced_Male_boolean, Widowed_Male_boolean, Never_Female_boolean, \
                    Married_Female_boolean, Separated_Female_boolean, Divorced_Female_boolean, Widowed_Female_boolean, \
                    Younger_than_6_only_boolean, Both_younger_than_6_between_6_and_17_boolean, 6_to_17_only_boolean) \
                    VALUES (%d, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %f, %f, %f, %f, %f, %f, %f, %f, %f, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                    %d, %d, %d, %d, %d, %d, %d, %d, %d)" % \
                    (zip, values_demographics[0], values_demographics[1], values_demographics[2], \
                    values_demographics[3], values_demographics[4], values_demographics[5], \
                    values_demographics[6], values_demographics[7], values_demographics[8], \
                    values_demographics[9], values_demographics[10], values_demographics[11], \
                    values_demographics[12], values_demographics[13], values_demographics[14], \
                    values_demographics[15], values_demographics[16], values_demographics[17], \
                    values_demographics[18], values_demographics[19], values_demographics[20], \
                    values_demographics[21], values_demographics[22], values_demographics[23], \
                    values_demographics[24], values_demographics[25], values_demographics[26], \
                    values_demographics[27], values_demographics[28], values_demographics[29], \
                    values_demographics[30], values_demographics[31], values_demographics[32], \
                    values_demographics[33], values_demographics[34], values_demographics[35], \
                    values_demographics[36], values_demographics[37], values_demographics[38], \
                    values_demographics[39], values_demographics[40], values_demographics[41], \
                    values_demographics[42], values_demographics[43], values_demographics[44], \
                    values_demographics[45], values_demographics[46], values_demographics[47], \
                    values_demographics[48], values_demographics[49], values_demographics[50], \
                    values_demographics[51], values_demographics[52], values_demographics[53], \
                    values_demographics[54], values_demographics[55], values_demographics[56], \
                    values_demographics[57], values_demographics[58], values_demographics[59], \
                    values_demographics[60], values_demographics[61], values_demographics[62], \
                    values_demographics[63], values_demographics[64], values_demographics[65], \
                    values_demographics[66], values_demographics[67], values_demographics[68], \
                    boolean_demographics[0], boolean_demographics[1], boolean_demographics[2], \
                    boolean_demographics[3], boolean_demographics[4], boolean_demographics[5], \
                    boolean_demographics[6], boolean_demographics[7], boolean_demographics[8], \
                    boolean_demographics[9], boolean_demographics[10], boolean_demographics[11], \
                    boolean_demographics[12], boolean_demographics[13], boolean_demographics[14], \
                    boolean_demographics[15], boolean_demographics[16], boolean_demographics[17], \
                    boolean_demographics[18], boolean_demographics[19], boolean_demographics[20], \
                    boolean_demographics[21], boolean_demographics[22], boolean_demographics[23], \
                    boolean_demographics[24], boolean_demographics[25], boolean_demographics[26], \
                    boolean_demographics[27], boolean_demographics[28], boolean_demographics[29], \
                    boolean_demographics[30], boolean_demographics[31], boolean_demographics[32], \
                    boolean_demographics[33], boolean_demographics[34], boolean_demographics[35], \
                    boolean_demographics[36], boolean_demographics[37], boolean_demographics[38], \
                    boolean_demographics[39], boolean_demographics[40], boolean_demographics[41], \
                    boolean_demographics[42], boolean_demographics[43], boolean_demographics[44], \
                    boolean_demographics[45], boolean_demographics[46], boolean_demographics[47], \
                    boolean_demographics[48], boolean_demographics[49], boolean_demographics[50], \
                    boolean_demographics[51], boolean_demographics[52], boolean_demographics[53], \
                    boolean_demographics[54], boolean_demographics[55], boolean_demographics[56], \
                    boolean_demographics[57], boolean_demographics[58], boolean_demographics[59], \
                    boolean_demographics[60], boolean_demographics[61], boolean_demographics[62], \
                    boolean_demographics[63], boolean_demographics[64], boolean_demographics[65], \
                    boolean_demographics[66], boolean_demographics[67], boolean_demographics[68]) 
    #        print sql
           # 执行sql语句
            cursor.execute(sql)
           # 提交到数据库执行
            db.commit()
        except:
           # Rollback in case there is any error
#           print '1'
            db.rollback()  





        
#        boolean_total = boolean_cost_of_living + boolean_crime + boolean_demographics + boolean_education + boolean_employment + boolean_housing + boolean_weather
#        values_total = values_cost_of_living + values_crime + values_demographics + values_education + values_employment + values_housing + values_weather
#        final = boolean_total + values_total
        
#        f=open('crawl_areavibes_result.txt', 'w')
#        f.write(str(final))
#        f=open('crawl_areavibes_result.txt', 'r')
        
        print "ZIP = %d Done!" % zip
#        # time.sleep(random.randint(1, 60))
        
    except:
       print "There is no info for %d" % zip    
   
# 关闭数据库连接
db.close()

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 02 13:43:31 2016

@author: Junxiao
"""


import MySQLdb
from sklearn.externals import joblib
import facebook
import json
import cookielib
import os
import urllib2
import urllib
from bs4 import BeautifulSoup


#%% input data
First_name      = 'Junxiao'
Last_name       = 'Zhu'
Email           = 'junxiaozhu@gmail.com'
Phone_num       = '8328677001'
Street_name     = 'Gulfton ST.'
House_number    = '5805'
Apartment_num   = '2916'
City            = 'Houston'
Zipcode         = '77081'
Amount          = '5200'
Annual_inc      = '30000'
Facebook_token  = ''
LinkedIn_acc    = ''

filename="result.txt" #The entire DOM of the page currently viewed is stored
path=os.path.split(__file__)[0]
if(os.path.isfile(os.path.join(path,filename))):
    os.remove(os.path.join(path,filename))
f=open(filename,"a")


#%% evaluate the application
# 打开数据库连接

#Database_ip = "172.25.31.146"
#db = MySQLdb.connect(Database_ip,"root","123456789o","MMT" )

db = MySQLdb.connect("localhost","root","123456789o","MMT" )


# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 获取model
clf = joblib.load('.\\Score\\Grade.pkl')
scaler = joblib.load('.\\Score\\scaler_std.pkl')

X = []

train_num = 1
# 构建每个数据的特征向量
for id in range(train_num):
    try:
#        sql = """SELECT * FROM  loandatabase WHERE id = %d""" % (int(Zipcode))
#        cursor.execute(sql)
#        results = cursor.fetchall()
#        for row in results:
        igeoid = int(Zipcode)
        famount = float(Amount)
        annual_income = float(Annual_inc)
        X.append([famount, annual_income])
        if annual_income:
            X[id].extend([famount/annual_income, 1])
        else:
            X[id].extend([0.0, 0])        
        # cost_of_living
        sql = """SELECT * FROM cost_of_living WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
            if float(row[1]):
                X[id].extend([famount/float(row[1]), 1])
            else:
                X[id].extend([0.0, 0])
            if float(row[2]):
                X[id].extend([famount/float(row[2]), 1])
            else:
                X[id].extend([0.0, 0])
            if float(row[3]):
                X[id].extend([famount/float(row[3]), 1])
            else:
                X[id].extend([0.0, 0])            
            if float(row[25]):
                X[id].extend([famount/float(row[25]), 1])
            else:
                X[id].extend([0.0, 0])              
        # Crime
        sql = """SELECT * FROM crime WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
        # Education
        sql = """SELECT * FROM education WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
        # Employment
        sql = """SELECT * FROM employment WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
            if float(row[1]):
                X[id].extend([famount/float(row[1]), 1])
            else:
                X[id].extend([0.0, 0])        
            
        # Housing
        sql = """SELECT * FROM housing WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
    
        # Weather
        sql = """SELECT * FROM weather WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
    except:
        temp = 0

X_test_transformed = scaler.transform(X)
predict_grade = clf.predict(X_test_transformed)[0]
letter_grade = ['A','B','C','D','E','F','G','H'][predict_grade - 1]
print 'Grade = ', letter_grade
print '#################'
#f.write(str(letter_grade))
json.dump(letter_grade,f)
f.write('\n')
#%% calculate the interest range
#sql = """SELECT MAX(int_rate) FROM  loandatabase WHERE grade = %d""" % predict_grade
#cursor.execute(sql)
#result = cursor.fetchone()
#int_max = round(result[0],2)
#
#
#sql = """SELECT MIN(int_rate) FROM  loandatabase WHERE grade = %d""" % predict_grade
#cursor.execute(sql)
#result = cursor.fetchone()
#int_min = round(result[0],2)

int_min = [5.32, 6.00, 6.00, 6.00, 6.00, 6.00, 6.00][predict_grade - 1]
int_max = [9.63, 14.09, 17.27, 21.49, 25.29, 27.79, 30.99][predict_grade - 1]

print 'Recommandation of interest range %.2f%% to %.2f%%' % (int_min,int_max)
print '#################'
#f.write(str(int_min))
#f.write(str(int_max))
json.dump(int_min,f)
f.write('\n')
json.dump(int_max,f)
f.write('\n')

#%% calculate the default rate
#sql = 'SELECT COUNT(*) from loandatabase WHERE grade = %d AND loan_status = -1' % predict_grade
#cursor.execute(sql)
#result = cursor.fetchone()
#default = float(result[0])*100
#sql = 'SELECT COUNT(*) from loandatabase WHERE grade = %d' % predict_grade
#cursor.execute(sql)
#result = cursor.fetchone()
#total_grade = float(result[0])
#default_rate = round(default/total_grade,2)

default_rate = [1.85, 4.11, 6.24, 9.63, 11.76, 15.76, 18.97][predict_grade - 1]

print 'Charged off rate = %.2f%%' % default_rate
print '#################'
#f.write(str(default_rate))
json.dump(default_rate,f)
f.write('\n')

#%% Facebook likes
# https://developers.facebook.com/tools/explorer/154061541706136?method=GET&path=me%3Ffields%3Did%2Cname%2Clikes%2Cemail&version=v2.7
try:
    token = 'EAACMHj93iZAgBALzPTdaG0NqgZBgWwWPA0dzArmmfTPuIiMJ76eiy6V8HpwU0Yj8J6S9LlI4G8kRPaCslFTeJhAQVcoKyZAWh01jXCiWibBIXZCoYKoCq2mAiCIjvLIv11TWstohhmfZApv7rz2bkZBq5UTUqWud6FZADubjn2bQQZDZD'
    myfbgraph = facebook.GraphAPI(token)
    mylikes = myfbgraph.get_connections(id="me", connection_name="likes")['data']
    test = myfbgraph.get_object(id = "me")
    print 'Facebook Likes:'
    json.dump('Facebook Likes:',f)
    f.write('\n')
    Facebook_likes = []
    for like in mylikes:
        Facebook_likes.append(str(like['name']))
        print like['name']
        json.dump(like['name'],f)
        f.write('\n')
    
except:
    print 'Session has expired!'
print '#################'
#f.write(str(Facebook_likes))

#%% Linkedin skills
#import getpass

username = 'junxiaozhu@gmail.com'#raw_input("Enter your linkedin username : ")
password = 'linkedin1qazse4'#getpass.getpass("Enter your linkedin password : ")


linkedin_link = 'https://www.linkedin.com/in/junxiao-zhu-35a26257'
#linkedin_link = 'https://www.linkedin.com/in/jiabiaoruan'


cookie_filename = "parser.cookies.txt" #Cookies set by linkedin are stored



class LinkedInParser(object):

    def __init__(self, login, password):
        if(os.path.isfile(os.path.join(path,cookie_filename))):
            os.remove(os.path.join(path,cookie_filename))
        """ Start up... """
        self.login = login
        self.password = password

        # Simulate browser with cookies enabled
        self.cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

        # Login
        self.loginPage()

        self.cj.save()


    def loadPage(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        # We'll print the url in case of infinite loop
        # print "Loading URL: %s" % url
        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            return ''.join(response.readlines())
        except:
            # If URL doesn't load for ANY reason, try again...
            # Quick and dirty solution for 404 returns because of network problems
            # However, this could infinite loop if there's an actual problem
            return self.loadPage(url, data)

    def loginPage(self):
        """
        Handle login. This should populate our cookie jar.
        """
        html = self.loadPage("https://www.linkedin.com/")
        soup = BeautifulSoup(html, "lxml")
        csrf = soup.find(id="loginCsrfParam-login")['value']
        login_data = urllib.urlencode({
            'session_key': self.login,
            'session_password': self.password,
            'loginCsrfParam': csrf,
        })

        html = self.loadPage("https://www.linkedin.com/uas/login-submit", login_data)
        return


    def loadpersonalpage(self):
        html=self.loadPage(linkedin_link)
        soup=BeautifulSoup(html, "lxml")

        x = str(soup.findAll(attrs={'id':['my_profile_post-content']}))
        skill_num = x.count('"url_skillSearch":"/vsearch/f?keywords=')
#        print 'skill_num=', skill_num
        start_index = 0
        global skill_vec 
        skill_vec = []
        for i in range(skill_num):
            skill_start = x.find('"url_skillSearch":"/vsearch/f?keywords=',start_index , -1) + 39
            skill_end = x.find('&trk=profile\\',skill_start,-1)
            skill_name = x[skill_start:skill_end]
            skill_name = skill_name.replace("+", " ")
            print skill_name
            json.dump(skill_name,f)
            f.write('\n')
            skill_vec.append(skill_name)
            start_index = skill_end + 1
#        f.write(str(skill_vec))

print 'LinkedIn skills:'
json.dump('LinkedIn skills:',f)
f.write('\n')
parser = LinkedInParser(username, password) #Creating an instance for LinkedInParser, and the constructor takes in username,password set above as parameters to login
parser.loadpersonalpage()
print '#################'

f.close()
# 关闭数据库连接
db.close()

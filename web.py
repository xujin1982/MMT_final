#coding:utf8
from werkzeug import secure_filename
from flask import Flask, render_template, flash
from flask_wtf import Form, RecaptchaField
from wtforms.fields import (StringField, PasswordField, DateField, BooleanField,
                            SelectField, SelectMultipleField, TextAreaField,
                            RadioField, IntegerField, DecimalField, SubmitField)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Regexp

import MySQLdb
from sklearn.externals import joblib
import facebook
import cookielib
import os
import urllib2
import urllib
from bs4 import BeautifulSoup

path=os.path.split(__file__)[0]


app = Flask(__name__)

app.config.update(
    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J',
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu',
    RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'},
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
)

class LoginForm(Form):
    user = StringField('Username', validators=[DataRequired()])

class AttachForm(Form):
    attach = FileField('Your Attachment', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

class SignupForm(Form):
    username = StringField('Username')
    recaptcha = RecaptchaField()


class RegisterForm(Form):
    # Text Field类型，文本输入框，必填，用户名长度为4到25之间
    First_name = StringField('First_name', validators=[Length(min=4, max=25)])

    # Text Field类型，文本输入框，必填，用户名长度为2到25之间
    Last_name = StringField('Last_name', validators=[Length(min=2, max=25)])
    
    # Text Field类型，文本输入框，Email格式
    Email = StringField('Email Address', validators=[Email()])

    # Text Field类型，文本输入框，必填，用户名长度为10到12之间
    Phone_num = StringField('Phone number', validators=[Length(min=10, max=12)])

    # Text Field类型，文本输入框，必填，街道名长度为4到25之间
    Street_name = StringField('Street name', validators=[Length(min=4, max=25)])

    # Text Field类型，文本输入框，必填，门牌号长度为1到4之间
    House_number = StringField('House number', validators=[Length(min=1, max=4)])
    
    # Text Field类型，文本输入框，必填，公寓号长度为1到4之间
    Apartment_num = StringField('Apartment No.', validators=[Length(min=1, max=4)])

    # Text Field类型，文本输入框，必填，城市名长度为4到25之间
    City = StringField('City', validators=[Length(min=4, max=25)])

    # Text Field类型，文本输入框，必填，邮编长度为4到6之间
    Zipcode = StringField('Zipcode', validators=[Length(min=3, max=6)])
    
    # Text Field类型，文本输入框，必须输入数值，显示时保留两位小数
    Amount = DecimalField('Amount', places=2)
    
    # Text Field类型，文本输入框，必须输入数值，显示时保留两位小数
    Annual_inc = DecimalField('Annual income', places=2)

    # Checkbox类型，加上default='checked'即默认是选上的
    accept_terms = BooleanField('I accept the Terms of Use', default='checked',
                                validators=[DataRequired()])

    # Submit按钮
    submit = SubmitField('Register')

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.user.data == 'admin':
            return 'Admin login successfully!'
        else:
            flash('Wrong user!')

    return render_template('login.html', form=form)


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db = MySQLdb.connect("localhost","root","123456789o","MMT" )
        cursor = db.cursor()
        # 获取model
        clf = joblib.load('.\\Score\\Grade.pkl')
        scaler = joblib.load('.\\Score\\scaler_std.pkl')
        
        X = []
        
        train_num = 1
        # 构建每个数据的特征向量
        for id in range(train_num):
            try:
                igeoid = int(form.Zipcode.data)
                famount = float(form.Amount.data)
                annual_income = float(form.Annual_inc.data)
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
#        print 'Grade = ', letter_grade
#        print '#################'

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
        
#        print 'Recommandation of interest range %.2f%% to %.2f%%' % (int_min,int_max)
#        print '#################'

        
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
        
#        print 'Charged off rate = %.2f%%' % default_rate
#        print '#################'
        #f.write(str(default_rate))

        #%% Facebook likes
        # https://developers.facebook.com/tools/explorer/154061541706136?method=GET&path=me%3Ffields%3Did%2Cname%2Clikes%2Cemail&version=v2.7
        try:
            token = 'EAACMHj93iZAgBACb1Hx8gnxtvkBbPve5YFnZBS51sDW5ymQnZBULcxdEuJDTl3muE8ciHPYsRmacSBIrkCIA8aUsMkoNsgnwcrFGI45QqN0VFh2H5A4epe7gpwQLgJj16ZBqkMYT1oNCQZCU9vz4Q4XDuG6uNfGPBbaofXO5lQwZDZD'
            myfbgraph = facebook.GraphAPI(token)
            mylikes = myfbgraph.get_connections(id="me", connection_name="likes")['data']
#            print 'Facebook Likes:'
            Facebook_likes = []
            for like in mylikes:
                Facebook_likes.append(str(like['name']))
#                print like['name']

            
        except:
            print 'Session has expired!'
#        print '#################'
        #f.write(str(Facebook_likes))
        
        #%% Linkedin skills
        #import getpass
        
        username1 = '321@gmail.com'#raw_input("Enter your linkedin username : ")
        password1 = '1234'#getpass.getpass("Enter your linkedin password : ")
       
        
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
#                    print skill_name

                    skill_vec.append(skill_name)
                    start_index = skill_end + 1
        #        f.write(str(skill_vec))
        


        parser = LinkedInParser(username1, password1) #Creating an instance for LinkedInParser, and the constructor takes in username,password set above as parameters to login
        parser.loadpersonalpage()

        
        flash('Grade: %s' % letter_grade)
        flash('Recommandation of interest range %.2f%% to %.2f%%' % (int_min,int_max))
        flash('Charged off rate: %.2f%%' % default_rate)
        flash('Total number of Facebook Likes: %d' % len(Facebook_likes))
        for temp in Facebook_likes:
            flash('- %s' % temp)
        flash('Total number of LinkedIn Skills: %d' % len(skill_vec))
        for temp in skill_vec:
            flash('- %s' % temp)        
        login_form = LoginForm()
        return render_template('login.html', form=login_form)

    return render_template('register.html', form=form)

app.secret_key = '1234567'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

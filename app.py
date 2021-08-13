#!/usr/bin/env python
# encoding: utf-8
'''
@author: ######
@file: app.py
@time: 2021/2/24 17:51
@software: PyCharm 2020.1.2(Professional Edition)
'''

from flask import Flask
import utils  # 数据库操作封装
from flask import render_template
from flask import request, flash, session, redirect, url_for
from flask import jsonify
import jieba.analyse  # 关键字提取的库
from dateutil.parser import parse  # 日期解析器 字符串转换为日期格式
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # 转换密码用到的库
from sqlalchemy import and_, or_
from flask_mail import Message, Mail
import random

# 初始化创建程序实例
app = Flask(__name__)

'''配置参数'''
# 数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/covid-19'
# 开启跟踪对象的修改并且发送信号
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# flask及相关扩展的加密密钥
app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'

# 实例化数据库对象
db = SQLAlchemy(app)

# 邮箱配置
# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
app.config['MAIL_SERVER'] = "smtp.qq.com"
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
# MAIL_USE_SSL
app.config['MAIL_USERNAME'] = "xxxxxxxxxxxx@qq.com"
app.config['MAIL_PASSWORD'] = "****************"  # 授权码
app.config['MAIL_DEFAULT_SENDER'] = "xxxxxxxxxxxx@qq.com"

# 实例化邮件对象
mail = Mail(app)

'''
数据库定义部分
'''
# 定义ORM
class User(db.Model):
    # 定义表名
    __tablename__ = 'cov_users'
    # 字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError("密码不允许读取")

    # 转换密码为hash存入数据库
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)


# 创建表格、插入数据
@app.before_first_request
def create_db():
    db.drop_all()  # 每次运行，先删除再创建
    db.create_all()

    admin = User(username='admin', password='root', email='admin@example.com')
    db.session.add(admin)

    guestes = [User(username='guest1', password='guest1', email='guest1@example.com'),
               User(username='guest2', password='guest2', email='guest2@example.com'),
               User(username='guest3', password='guest3', email='guest3@example.com'),
               User(username='guest4', password='guest4', email='guest4@example.com')]
    db.session.add_all(guestes)
    db.session.commit()


'''
辅助函数、装饰器
'''
# 登录检验（用户名、密码验证）
def valid_login(username, password):
    # str1 = check_password_hash(User.password, password)
    # user = User.query.filter(and_(User.username == username, str1)).first()
    # if user:
    #     return True
    # else:
    #     return False
    user = User.query.filter(User.username == username).first()
    if user:
        if user.check_password_hash(password):
            return True
        else:
            return False
    return False


# 注册检验（用户名、邮箱验证）
def valid_regist(username, email):
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if user:  # 若已经存在重复的用户名或邮箱
        return False
    else:
        return True


@app.route('/')
# 首页
@app.route('/index')
def index():
    return render_template('index.html', username=session.get('username'))

# 显示时间 实时刷新
@app.route("/time")
def flush_time():
    return utils.flush_time()


''' 
返回国内最新的新冠疫情病例数据（来源：腾讯新闻，https://news.qq.com/zt2020/page/feiyan.htm#/）     
'''
# 累计确诊、累计治愈、累计死亡、现存确诊
@app.route("/c1")
def get_c1_data():
    data = utils.get_c1_data()
    return jsonify({
        "confirm": data[0], "heal": data[1],
        "dead": data[2], "nowConfirm": data[3]
    })


'''
返回国内新冠疫情的历史数据
'''
@app.route('/c2')
def get_c2_data():
    tup = utils.get_c2_data()
    res = []
    for i in range(len(tup)):
        res.append({
            "name": tup[i][0],
            "value": int(tup[i][1])
        })
    return jsonify({"data": res})


'''
返回国内新冠疫情的累计趋势
'''
# 累计确诊、累计治愈、累计死亡、现存确诊
@app.route('/l1')
def get_l1_data():
    data = utils.get_l1_data()
    dateID, confirmedCount, curedCount, deadCount, currentConfirmedCount = [], [], [], [], []
    for a, b, c, d, e in data:
        str1 = parse(str(a))
        dateID.append(str1.strftime("%m-%d"))
        confirmedCount.append(b)
        curedCount.append(c)
        deadCount.append(d)
        currentConfirmedCount.append(e)
    return jsonify({
        "dateID": dateID,
        "confirmedCount": confirmedCount,
        "curedCount": curedCount,
        "deadCount": deadCount,
        "currentConfirmedCount": currentConfirmedCount
    })


'''
返回国内新冠疫情的新增趋势
'''
# 新增确诊、新增治愈
@app.route('/l2')
def get_l2_data():
    data = utils.get_l2_data()
    dateID, confirmedIncr, curedIncr = [], [], []
    for a, b, c in data:
        str1 = parse(str(a))
        dateID.append(str1.strftime("%m-%d"))
        confirmedIncr.append(b)
        curedIncr.append(c)
    return jsonify({
        "dateID": dateID,
        "confirmedIncr": confirmedIncr,
        "curedIncr": curedIncr
    })


'''
返回全球新冠疫情现存确诊TOP5
'''
# 国家简称、现存确诊
@app.route('/r1')
def get_r1_data():
    data = utils.get_r1_data()
    provinceName = []
    currentConfirmedCount = []
    for k, v in data:
        provinceName.append(k)
        currentConfirmedCount.append(int(v))
    return jsonify({
        "provinceName": provinceName,
        "currentConfirmedCount": currentConfirmedCount
    })


'''
返回国内关于新冠疫情的实时热搜（来源：百度热搜，https://voice.baidu.com/act/newpneumonia/newpneumonia?fraz=partner&paaz=gjyj）
'''
@app.route('/r2')
def get_r2_data():
    data = utils.get_r2_data()
    d = []
    for i in range(len(data)):
        item = data[i][0]
        jieba.analyse.set_stop_words('./static/baidu_stopwords.txt')  # 利用停止词对热搜进行过滤
        # 根据TF-IDF算法提取关键字
        keywords = jieba.analyse.extract_tags(item, topK=20, withWeight=True, allowPOS=())
        for k, v in keywords:
                d.append({
                    "name": k,
                    "value": str(int(v * 100))
                })
    return jsonify({"kws": d})

# 登录页
@app.route('/login', methods=['GET', 'POST'])
def login():
    # error = None
    if request.method == 'POST':
        name = request.form['username']
        psw = request.form['password']
        if valid_login(name, psw):
            session['username'] = request.form.get('username')
            # return redirect(url_for('index'))
            return render_template('main.html')  # 登陆成功，返回可视化平台页面
        else:
            flash("错误的用户名或密码！")

    # return render_template('login.html',error=error)
    return render_template('login.html')

# 注销
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))  # 注销登录，返回首页

# 注册
@app.route('/register', methods=['GET', 'POST'])
def register_form():
    # error = None
    if request.method == 'POST':
        if valid_regist(request.form['username'], request.form['email']):
            if session['code'] == request.form['code']:
                user = User(username=request.form['username'], password=request.form['password'],
                            email=request.form['email'])
                db.session.add(user)
                db.session.commit()
                flash("成功注册！")
                return redirect(url_for('login'))
            else:
                flash("邮箱验证码错误！")
        else:
            flash("该用户名或邮箱已被注册！")

    return render_template('register.html')


# 验证码生成函数
def generate_code(len=6):
    ''' 随机生成6位的验证码 '''
    # 生成的是0-9A-Za-z的列表
    code_list = []
    for i in range(10):  # 0-9 数字
        code_list.append(str(i))
    for i in range(65, 91):  # 对应从A到Z的ASCII码
        code_list.append(chr(i))
    for i in range(97, 123):  # 对应从a到z的ASCII码
        code_list.append(chr(i))
    print(code_list)
    str1 = random.sample(code_list, len)  # 从list中随机获取6个元素，作为一个片断返回
    print(str1)
    code = ''.join(str1)  # 列表转字符
    # print(code)
    return code


# 邮件发送函数
def email_captcha():
    email = request.form['email']
    if not email:
        return False
    '''
    生成随机验证码，保存到内存中，然后发送验证码，与用户提交的验证码对比
    '''
    captcha = generate_code()  # 随机生成6位验证码
    # 给用户提交的邮箱发送邮件
    # message = Message('COVID-19数据可视化平台邮箱验证码', recipients=[email], body='您的验证码是：%s' % captcha)
    message = Message('COVID-19数据可视化平台邮箱验证码', recipients=[email], body=render_template("code.html", code=captcha))
    try:
        mail.send(message)  # 发送
        session['code'] = captcha
    except:
        return False


# 程序入口
if __name__ == '__main__':
    app.run(debug=False)

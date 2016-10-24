# -*- coding: utf-8 -*-

import hashlib
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

url = 'http://223.2.10.26/cas/logon.action'
url2 = 'http://223.2.10.26/cas/genValidateCode'
url3 = 'http://223.2.10.26/frame/jw/teacherstudentmenu.jsp?menucode=JW1314'
url4 = 'http://223.2.10.26/student/xscj.stuckcj.jsp?menucode=JW130706'
url5 = 'http://223.2.10.26/jw/common/showYearTerm.action'
url6 = 'http://223.2.10.26/student/xscj.stuckcj_data.jsp'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

header1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'Referer': url3}

header2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'Referer': url4}

def md5(str):
    import hashlib
    import types
    if type(str) is types.StringType:
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()
    else:
        return ''

print u'南师大教务系统快速查分（控制台版）'

username = raw_input(u'请输入你的学号：'.encode('gbk'))
pwd = raw_input(u'请输入你的密码：'.encode('gbk'))

s = requests.session()
r = s.get(url2, headers=header)
im = Image.open(BytesIO(r.content))
im.show()

yzm = raw_input(u'请输入验证码：'.encode('gbk'))

data = {
    'username': username,
    'password': md5(md5(pwd) + md5(yzm)),
    'randnumber': yzm,
    'isPasswordPolicy': '1'
}
s.post(url, data, headers=header)

p = s.post(url5, headers=header)
userCode = p.json()['userCode']

s.get(url3, headers=header)
s.get(url4, headers=header1)

data2 = {
    'sjxz': 'sjxz1',
    'ysyx': 'yxcj',
    'userCode': userCode, 
    'xn1': '2017',
    'ysyxS': 'on',
    'sjxzS': 'on',
    'menucode_current': ''
}

f = s.post(url6, data2, headers=header2)

soup = BeautifulSoup(f.text,'html.parser')

info=list()
table = soup.find('div',group='group').find_all('div')
for i in table:
    info.append(i.string.split(u'：')[1])

thead = [u'序号',u'课程/环节',u'学分',u'类别',u'修读性质',u'考核方式',u'成绩',u'获得学分',u'绩点',u'学分绩点',u'备注']

term = list()
a = soup.find_all('td', style='border: none;width:25%;')
for i in a:
    term.append(i.string.split(u'：')[1])

grade=list()
tb = soup.find_all('table', style='clear:left;width:256mm;font-size:12px;')
for i in tb:
    t = i.find('tbody').find_all('tr')
    temp1=list()
    temp1.append(thead)
    for j in t:
        g = j.find_all('td')
        temp2=list()
        for k in g:
            temp2.append(k.string)
        temp1.append(temp2)
    grade.append(temp1)

print ''
print u'院(系)/部：',info[0]
print u'行政班级：',info[1]
print u'学号：',info[2]
print u'姓名：',info[3]
print u'打印时间：',info[4]
print ''
for i in range(0,len(term)):
    print term[i]
    for e in grade[i]:
        for r in e:
            if r==None:
                r=u'无'
            print r,'',
        print ''
    print ''

raw_input(u'查询完毕！按任意键退出……'.encode('gbk'))
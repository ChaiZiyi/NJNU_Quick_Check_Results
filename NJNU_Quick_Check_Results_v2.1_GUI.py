# -*- coding: UTF-8 -*-

import wx
import requests
import hashlib
from cStringIO import StringIO
from bs4 import BeautifulSoup
import sys

url = 'http://223.2.10.23/cas/logon.action'
url2 = 'http://223.2.10.23/cas/genValidateCode'
url3 = 'http://223.2.10.23/frame/jw/teacherstudentmenu.jsp?menucode=JW1314'
url4 = 'http://223.2.10.23/student/xscj.stuckcj.jsp?menucode=JW130706'
url5 = 'http://223.2.10.23/jw/common/showYearTerm.action'
url6 = 'http://223.2.10.23/student/xscj.stuckcj_data.jsp'

photourl = 'http://223.2.10.123/jwgl/photos/rx20'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

header1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'Referer': url3}

header2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'Referer': url4}

s = requests.Session()


def getValidateCode():
    r = s.get(url2, headers=header)
    image = wx.ImageFromStream(
        StringIO(r.content), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    return image


def getStatus(username, pwd, yzm):
    data = {
        'username': username,
        'password': hashlib.md5(hashlib.md5(pwd).hexdigest() + hashlib.md5(yzm).hexdigest()).hexdigest(),
        'randnumber': yzm,
        'isPasswordPolicy': '1'
    }
    t = s.post(url, data, headers=header)
    return t.json()


def getResults():
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

    soup = BeautifulSoup(f.text, 'html.parser')

    info = list()
    table = soup.find('div', group='group').find_all('div')
    for i in table:
        info.append(i.string)
    info.append(u'查询完毕!')

    term = list()
    a = soup.find_all('td', style='border: none;width:25%;')
    for i in a:
        term.append(i.string.split(u'：')[1])

    grade = list()
    num = 0
    tb = soup.find_all('table', style='clear:left;width:256mm;font-size:12px;')
    for i in tb:
        t = i.find('tbody').find_all('tr')
        for j in t:
            g = j.find_all('td')
            temp = list()
            temp.append(term[num])
            for k in g:
                if k.string == None:
                    temp.append('')
                else:
                    temp.append(k.string)
            grade.append(temp)
        num += 1

    return (info, grade)


class MyFrame(wx.Frame):

    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, None, size=(1200, 600))
        self.panel = wx.Panel(self)
        self.label_1 = wx.StaticText(self.panel, wx.ID_ANY, u'学号')
        self.text_ctrl_1 = wx.TextCtrl(
            self.panel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.label_2 = wx.StaticText(self.panel, wx.ID_ANY, u'密码')
        self.text_ctrl_2 = wx.TextCtrl(
            self.panel, wx.ID_ANY, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.label_3 = wx.StaticText(self.panel, wx.ID_ANY, u'验证码')
        self.text_ctrl_3 = wx.TextCtrl(
            self.panel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.bitmap_button_1 = wx.BitmapButton(
            self.panel, wx.ID_ANY, getValidateCode())
        self.button_1 = wx.Button(self.panel, wx.ID_ANY, u'重置', size=(70, 30))
        self.button_2 = wx.Button(self.panel, wx.ID_ANY, u'查询', size=(70, 30))
        self.text_ctrl_4 = wx.TextCtrl(
            self.panel, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.static_bitmap_1 = wx.StaticBitmap(
            self.panel, wx.ID_ANY, size=(105, 147))
        self.list_ctrl_1 = wx.ListCtrl(
            self.panel, wx.ID_ANY, style=wx.LC_REPORT)

        self.SetTitle(u'南师大教务系统快速查分')

        self.__do_layout()

        self.bitmap_button_1.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.button_1.Bind(wx.EVT_BUTTON, self.OnClear)
        self.button_2.Bind(wx.EVT_BUTTON, self.OnSubmit)
        self.text_ctrl_1.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
        self.text_ctrl_2.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)
        self.text_ctrl_3.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)

        self.Centre()

    def __do_layout(self):

        sizer = wx.GridBagSizer(0, 0)

        sizer.Add(self.label_1, (0, 0), (1, 1), wx.ALL, 5)
        sizer.Add(self.text_ctrl_1, (0, 1), (1, 2), wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.label_2, (1, 0), (1, 1), wx.ALL, 5)
        sizer.Add(self.text_ctrl_2, (1, 1), (1, 2), wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.label_3, (2, 0), (1, 1), wx.ALL, 5)
        sizer.Add(self.text_ctrl_3, (2, 1), (1, 1), wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.bitmap_button_1, (2, 2), (1, 1), wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.button_1, (3, 1), (1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)
        sizer.Add(self.button_2, (3, 2), (1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)
        sizer.Add(self.static_bitmap_1, (0, 3), (4, 1), wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.text_ctrl_4, (0, 4), (4, 1), wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.list_ctrl_1, (4, 0), (1, 5), wx.EXPAND | wx.ALL, 5)

        sizer.AddGrowableRow(4, 1)
        sizer.AddGrowableCol(4, 1)

        self.panel.SetSizerAndFit(sizer)

    def OnClicked(self, event):
        self.bitmap_button_1.SetBitmapLabel(getValidateCode())

    def OnClear(self, event):
        self.text_ctrl_1.Clear()
        self.text_ctrl_2.Clear()
        self.text_ctrl_3.Clear()
        self.text_ctrl_4.Clear()
        self.static_bitmap_1.Hide()
        self.list_ctrl_1.ClearAll()
        self.bitmap_button_1.SetBitmapLabel(getValidateCode())

    def OnSubmit(self, event):

        self.static_bitmap_1.Hide()
        self.list_ctrl_1.ClearAll()
        username = self.text_ctrl_1.GetValue()
        pwd = self.text_ctrl_2.GetValue()
        yzm = self.text_ctrl_3.GetValue()
        status = getStatus(username, pwd, yzm)
        self.text_ctrl_4.SetValue(status['message'])
        if status['status'] == '200':
            year = username[2:4]
            name = username + '.jpg'
            turl = photourl + year + '/' + name
            req = requests.get(turl, headers=header)
            if req.headers.get('content-length') != '1163':
                image = wx.ImageFromStream(StringIO(req.content), wx.BITMAP_TYPE_ANY)
                image = image.Scale(105, 147, wx.IMAGE_QUALITY_HIGH)
                result = wx.BitmapFromImage(image)
                self.static_bitmap_1.SetBitmap(result)
                self.static_bitmap_1.Show()
            info = getResults()[0]
            for i in info:
                self.text_ctrl_4.AppendText('\n' + i)

            self.list_ctrl_1.InsertColumn(0, u'学期')
            self.list_ctrl_1.InsertColumn(1, u'序号')
            self.list_ctrl_1.InsertColumn(2, u'课程/环节')
            self.list_ctrl_1.InsertColumn(3, u'学分')
            self.list_ctrl_1.InsertColumn(4, u'类别')
            self.list_ctrl_1.InsertColumn(5, u'修读性质')
            self.list_ctrl_1.InsertColumn(6, u'考核方式')
            self.list_ctrl_1.InsertColumn(7, u'成绩')
            self.list_ctrl_1.InsertColumn(8, u'获得学分')
            self.list_ctrl_1.InsertColumn(9, u'绩点')
            self.list_ctrl_1.InsertColumn(10, u'学分绩点')
            self.list_ctrl_1.InsertColumn(11, u'备注')

            results = getResults()[1]
            for i in results:
                index = self.list_ctrl_1.InsertStringItem(sys.maxint, i[0])
                for j in range(1, 12):
                    self.list_ctrl_1.SetStringItem(index, j, i[j])
            for k in range(0, 12):
                self.list_ctrl_1.SetColumnWidth(k, wx.LIST_AUTOSIZE_USEHEADER)

        self.bitmap_button_1.SetBitmapLabel(getValidateCode())

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()

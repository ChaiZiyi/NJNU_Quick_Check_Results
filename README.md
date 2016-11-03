# NJNU_Quick_Check_Results 南师大教务系统快速查分

## v3.0

去掉了验证码，然后还加了左上角的小图标，但是，因为识别验证码要依赖tesseract-ocr这个库，试了一下午都不能把tesseract-ocr这个库打包进exe，所以用Pyinstaller生成的exe并不能直接用，还是要在客户机上装完tesseract-ocr才能用，所以这次的exe就不放上来了，后面做成web就可以完美避开这个问题了。果然客户端没前途……

### 正确查询界面

![](http://i.imgur.com/JMr5kbD.png)

## v2.1
把上次那个查看证件照GUI小程序的功能加进来了，查成绩时可以看到自己的证件照，然后改正了重置按钮的功能（以前只能重置3个输入框，现在可以全部重置了）

### 正确查询界面

![](http://i.imgur.com/p4cBLoj.png)

## v2.0
第一个GUI版本，至少不像之前控制台版那么丑了

### 正确查询界面

![](http://i.imgur.com/U9hR62a.png)

### 账号或密码输错界面

![](http://i.imgur.com/3fdB8pH.png)

### 验证码输错界面

![](http://i.imgur.com/L3ZxmMu.png)

## v1.1
1.1版把输入密码换成了星号显得更加安全，然后加上了验证码和账号密码输错的错误输出，不会像上一个版本直接崩溃。不过两个版本都有一个问题就是最后其实是要按回车键才能退出，写成任意键了……

### 正确查询界面

![](http://i.imgur.com/kXW5k4P.png)

### 账号或密码输错界面

![](http://i.imgur.com/pvp4Yjy.png)

### 验证码输错界面

![](http://i.imgur.com/yqgU7h7.png)

## v1.0
1.0版只是简单的实现了查询教务系统成绩的功能，没有用GUI界面，没有去掉验证码，也没有加上错误判断

### 正确查询界面

![](http://i.imgur.com/vHlV0uY.png)

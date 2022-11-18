#!/usr/bin/python3
# coding=utf-8
import urllib3
import json
import datetime as dt
import time
import sys

baseURL = "http://tiptime-api.com"
# 发送短信验证码
sendSmsUrl = baseURL + "/web/api/v2/login/code"
loginUrl = baseURL + "/web/api/login"


# 获取图片验证码


# 发送短信验证码！
def sendSmsCode(phone):
    print(phone)
    body_json = "phone=" + phone + ", captchaId=    , captchaCode=  "
    encoded_body = body_json.encode('utf-8')
    http = urllib3.PoolManager()
    header = {"User-Agent": "Dart/2.17 (dart:io)", "Host": "tiptime-api.com", "Platform": "android",
              "Content-Type": "application/json"}
    response = http.request('POST', sendSmsUrl, body=encoded_body, headers=header)
    if response.status != 201 and response.status != 200:
        print("getCode方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)

    if data['errCode'] != 0:
        print("请输入正确的手机号码！")
        exit()
    data = data['data']
    return


# 获取Authorization
def getAuthorization(phone, authCode):
    body_json = "?phone=" + phone + "&authCode=" + authCode
    encoded_body = body_json.encode('utf-8')
    header = {"User-Agent": "Dart/2.17 (dart:io)", "Host": "tiptime-api.com", "Platform": "android",
              "Content-Type": "application/x-www-form-urlencoded"}
    http = urllib3.PoolManager()
    response = http.request('POST', loginUrl, body=encoded_body, headers=header)
    if response.status != 201 and response.status != 200:
        print("getAuthorization方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)

    if data['errCode'] != 0:
        print("验证码错误!等待1分钟后重新运行再次获取验证码！\n")
        exit()
    data = data['data']

    return data['token']


# ********************************main******************************************
path = sys.path[0]
phonenum = input("请输入手机号码回车键提交:\n")
phonenum = str(phonenum)
if len(phonenum) != 11:
    print("手机号码不足或超出11位！\n请重新运行")
    exit()
sendSmsCode(phonenum)
print("验证码发送成功请耐性等待！\n")
authCode = input("请确保你输入验证码短信是甜糖发的验证码短信，以免造成经济损失，概不负责。\n请输入验证码：\n")
authCode = str(authCode)
if len(authCode) != 6:
    print("请输入正确的6位验证码!!\n请重新运行")
    exit()
authorization = getAuthorization(phonenum, authCode)
print("你的authorization：\n\n" + authorization + "\n\n")

sckey = input("请进入http://sc.ftqq.com/登录并绑定微信后获取sckey!\n请输入你的server酱的sckey码：\n")
config = {}
config["authorization"] = authorization
config["sckey"] = sckey
try:
    file = open(path + "/TTnodeConfig.conf", "w+", encoding="utf-8", errors="ignore")
    file.write(str(config))
    file.flush()
finally:
    if file:
        file.close()
print("已配置成功！\n请用python执行AutoTTnodeClient.py文件，以及配置定时程序。")
exit()

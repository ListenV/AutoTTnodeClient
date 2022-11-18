#!/usr/bin/python3
# coding=utf-8
import urllib3
import json
import datetime as dt
import time
import sys

devices = ''
inactivedPromoteScore = 0
total = 0
accountScore = 0
msgTitle = "【甜糖星愿】日结详细"
msg = "\n"
# API域名
baseURL = "http://tiptime-api.com"
# 获取验证码
GetCaptchaImageUrl = baseURL + "/api/v1/captcha/request"
# 发送短信
SendSmsUrl = baseURL + "/web/api/v2/login/code"
# 验证短信
VerifySmsCodeUrl = baseURL + "/web/api/login"
# 用户信息
UserInfoUrl = baseURL + "/web/api/account/message/loading"
# 每日签到
DailySignInUrl = baseURL + "/web/api/account/sign_in"
# 刷新登陆时间
RefreshLogin = baseURL + "/api/v1/login"

devicesListUrl = baseURL + "/api/v1/devices?page=1&per_page=20"
collect_rewards_url = baseURL + "/api/v1/score_logs"

# 使用 QMSG 通知
def sendQMSG(msg):
    url = "https://qmsg.zendee.cn/send/584ebe94943d833310a421e090c697c9"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    body_json = "msg=" + msg
    encoded_body = body_json.encode('utf-8')
    http = urllib3.PoolManager()
    response = http.request('POST', url, body=encoded_body, headers=header)
    if response.status != 200:
        print("sendQMSG方法请求失败，结束程序")
        data = response.data.decode('utf-8')
        data = json.loads(data)
        print(data)
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)
    return


# 使用 PushPlus 通知
def sendPushPlus(text, desp):
    url = "http://www.pushplus.plus/send"
    header = {"Content-Type": "application/json"}
    body_json = {"token": PushPlus_token, "title": text, "content": desp, "template": "html"}
    encoded_body = json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response = http.request('POST', url, body=encoded_body, headers=header)
    if response.status != 200:
        print("sendPushPlus方法请求失败，结束程序")
        logging.debug("sendPushPlus方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)
    print("消息已经推送至PushPlus，请注意查验！")
    return


# 使用 Server 酱通知
def sendServerJiang(text, desp):
    url = "https://sc.ftqq.com/" + sckey + ".send"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    body_json = "text=" + text + "&" + "desp=" + desp
    encoded_body = body_json.encode('utf-8')
    http = urllib3.PoolManager()
    response = http.request('POST', url, body=encoded_body, headers=header)
    if response.status != 200:
        print("sendServerJiang方法请求失败，结束程序")
        data = response.data.decode('utf-8')
        data = json.loads(data)
        print(data)
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)
    return


# 获取甜糖用户信息，可以获取待收取的推广信息数，可以获取账户星星数
def getUserInfo():
    header = {"Content-Type": "application/json", "authorization": authorization}
    http = urllib3.PoolManager()
    response = http.request('POST', UserInfoUrl, headers=header)
    if response.status != 200:
        print("getUserInfo方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)
    if data['errCode'] != 0:
        print("开始推送通知，authorization已经失效！")
        sendServerJiang("【甜糖星愿】-Auth失效通知",
                        "#### authorization已经失效，请重新抓包填写!\n")
        exit()
    data = data['data']
    return data


# 获取设备列表，可以获取待收的星星数
def getDeviceList():
    header = {"User-Agent": "Dart/2.17 (dart:io)", "Host": "tiptime-api.com", "Platform": "android",
              "Content-Type": "application/x-www-form-urlencoded", "authorization": authorization}
    http = urllib3.PoolManager()
    response = http.request('GET', devicesListUrl, headers=header)
    if response.status != 200:
        print("getDeviceList方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)
    if data['errCode'] != 0:
        print("开始推送通知，authorization已经失效！")
        sendServerJiang("【甜糖星愿】-Auth失效通知",
                        "#### authorization已经失效，请重新抓包填写!\n")
        exit()

    data = data['data']['data']
    if len(data) == 0:
        sendServerJiang("【甜糖星愿】请绑定通知",
                        "#### 该账号尚未绑定设备，请绑定设备后再运行！\n")
        exit()
    return data


# 收取推广奖励星星
def promote_score_logs(score):
    global msg
    if score == 0:
        msg = msg + "\n 【推广奖励】0-🌟\n"
        return
    url = "http://tiantang.mogencloud.com/api/v1/promote/score_logs"
    header = {"Content-Type": "application/json", "authorization": authorization}
    body_json = {'score': score}
    encoded_body = json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response = http.request('POST', url, body=encoded_body, headers=header)
    if response.status != 201 and response.status != 200:
        print("promote_score_logs方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)

    if data['errCode'] != 0:
        msg = msg + "\n 【推广奖励】0-🌟\n"
        return
    msg = msg + "\n 【推广奖励】" + str(score) + "-🌟\n"
    global total
    total = total + score
    data = data['data']
    # 发送微信推送，啥设备，获取了啥星星数
    return


# 收取设备奖励
def collect_rewards(device_id, score, name):
    global msg
    if score == 0:
        msg = msg + "\n 【" + name + "】0-🌟\n"
        return
    header = {"Content-Type": "application/json", "authorization": authorization}
    body_json = {'device_id': device_id, 'score': score}
    encoded_body = json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response = http.request('POST', collect_rewards_url, body=encoded_body, headers=header)
    if response.status != 201 and response.status != 200:
        print("score_logs方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)

    if data['errCode'] != 0:
        msg = msg + "\n 【" + name + "】0-🌟\n"
        return
    msg = msg + "\n 【" + name + "】" + str(score) + "-🌟\n"
    global total
    total = total + int(score)
    data = data['data']
    # 发送微信推送，啥设备，获取了啥星星数
    return


# 签到功能
def sign_in():
    header = {"User-Agent": "Dart/2.17 (dart:io)", "Host": "tiptime-api.com", "Platform": "android",
              "Content-Type": "application/x-www-form-urlencoded", "authorization": authorization}
    http = urllib3.PoolManager()
    response = http.request('POST', DailySignInUrl, headers=header)
    if response.status != 201 and response.status != 200:
        print("sign_in方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)
    global msg
    if data['errCode'] != 0:
        msg = msg + "\n 【签到失败】：" + data['msg'] + "\n"
        return
    msg = msg + "\n 【签到成功】2-🌟 \n"
    global total
    total = total + 2
    return


def readConfig(filePath):
    try:
        file = open(filePath, "a+", encoding="utf-8", errors="ignore")
        file.seek(0)
        result = file.read()
    finally:
        if file:
            file.close()
            print("文件流已经关闭")
    return result


# ********************************* main *************************************
path = sys.path[0]  # 脚本所在目录
config = readConfig(path + "/TTnodeConfig.conf")
print("config:" + config)

if len(config) == 0:
    print("错误提示：\nTTnodeConfig.conf为空！请重新运行TTnodeLogin.py")
    exit()

config = eval(config)  # 转成字典
authorization = config.get("authorization", "")
sckey = config.get("sckey", "")
if len(authorization) == 0:
    print("错误提示：\nauthorization为空，请重新运行TTnodeLogin.py")
    exit()
if len(sckey) == 0:
    print("错误提示：\nSckey为空，请重新运行TTnodeLogin.py")
    exit()
authorization = authorization.strip()
sckey = sckey.strip()

data = getUserInfo()
time.sleep(1)
inactivedPromoteScore = data['inactivedPromoteScore']
accountScore = data['score']

devices = getDeviceList()
time.sleep(1)
msg = msg + "\n#### 【收益详细】：\n```python"
promote_score_logs(inactivedPromoteScore)

# 执行签到
sign_in()
time.sleep(1)

for device in devices:
    collect_rewards(device['hardware_id'], device['inactived_score'], device['alias'])
    time.sleep(1)

total_str = "\n#### 【总共收取】" + str(total) + "-🌟\n"
newdata = getUserInfo()
accountScore = newdata['score']
accountScore_str = "\n#### 【账户星星】" + str(accountScore) + "-🌟\n"

end = "\n```\n***\n注意:以上统计仅供参考，一切请以甜糖客户端APP为准"
now_time = dt.datetime.now().strftime('%F %T')
now_time_str = "\n***\n#### 【当前时间】" + now_time + "\n"
msg = now_time_str + accountScore_str + total_str + msg + end
sendQMSG(msg)
# sendServerJiang(msgTitle,msg)
print("微信消息已推送。请注意查看。")
exit()

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


def sendPushPlus(text, desp):  # 发送PushPlus代码
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


def sendServerJiang(text, desp):  # 发送server酱代码
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


def getInitInfo():  # 甜糖用户初始化信息，可以获取待收取的推广信息数，可以获取账户星星数
    url = "http://tiantang.mogencloud.com/web/api/account/message/loading"
    header = {"Content-Type": "application/json", "authorization": authorization}
    http = urllib3.PoolManager()
    response = http.request('POST', url, headers=header)
    if response.status != 200:
        print("getInitInfo方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)
    if data['errCode'] != 0:
        print("发送推送微信，authorization已经失效")
        sendServerJiang("【甜糖星愿】-Auth失效通知",
                        "#### authorization已经失效，请重新抓包填写!\n填写邀请码123463支持作者！\n")
        exit()
    data = data['data']

    return data


def getDevices():  # 获取当前设备列表，可以获取待收的星星数
    url = "http://tiantang.mogencloud.com/api/v1/devices?page=1&type=2&per_page=200"
    header = {"Content-Type": "application/json", "authorization": authorization}
    http = urllib3.PoolManager()
    response = http.request('GET', url, headers=header)
    if response.status != 200:
        print("getDevices方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)
    if data['errCode'] != 0:
        print("发送推送微信，authorization已经失效")
        exit()

    data = data['data']['data']
    if len(data) == 0:
        sendServerJiang("【甜糖星愿】请绑定通知",
                        "#### 该账号尚未绑定设备，请绑定设备后再运行！\n填写邀请码123463支持作者！\n")
        exit()
    return data


def promote_score_logs(score):  # 收取推广奖励星星
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


def score_logs(device_id, score, name):  # 收取设备奖励
    global msg
    if score == 0:
        msg = msg + "\n 【" + name + "】0-🌟\n"
        return
    url = "http://tiantang.mogencloud.com/api/v1/score_logs"
    header = {"Content-Type": "application/json", "authorization": authorization}
    body_json = {'device_id': device_id, 'score': score}
    encoded_body = json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response = http.request('POST', url, body=encoded_body, headers=header)
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


def sign_in():  # 签到功能
    url = "http://tiantang.mogencloud.com/web/api/account/sign_in"
    header = {"Content-Type": "application/json", "authorization": authorization}
    http = urllib3.PoolManager()
    response = http.request('POST', url, headers=header)
    if response.status != 201 and response.status != 200:
        print("sign_in方法请求失败，结束程序")
        exit()
    data = response.data.decode('utf-8')
    data = json.loads(data)
    global msg
    if data['errCode'] != 0:
        msg = msg + "\n 【签到奖励】0-🌟(失败:" + data['msg'] + ")\n"
        return
    msg = msg + "\n 【签到奖励】1-🌟 \n"
    global total
    total = total + 1
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


# *********************************main*************************************
path = sys.path[0]  # 脚本所在目录
config = readConfig(path + "/TTnodeConfig.conf")
print("config:" + config)

if len(config) == 0:
    print("错误提示TTnodeConfig.conf为空，请重新运行TTnodeLogin.py")
    exit()

config = eval(config)  # 转成字典
authorization = config.get("authorization", "")
sckey = config.get("sckey", "")
if len(authorization) == 0:
    print("错误提示authorization为空，请重新运行TTnodeLogin.py")
    exit()
if len(sckey) == 0:
    print("错误提示sckey为空，请重新运行TTnodeLogin.py")
    exit()
authorization = authorization.strip()
sckey = sckey.strip()

data = getInitInfo()
time.sleep(1)
inactivedPromoteScore = data['inactivedPromoteScore']
accountScore = data['score']

devices = getDevices()
time.sleep(1)
msg = msg + "\n#### 【收益详细】：\n```python"
promote_score_logs(inactivedPromoteScore)

sign_in()
time.sleep(1)

for device in devices:
    score_logs(device['hardware_id'], device['inactived_score'], device['alias'])
    time.sleep(1)

total_str = "\n#### 【总共收取】" + str(total) + "-🌟\n"
newdata = getInitInfo()
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
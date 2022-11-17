## 介绍

甜糖自动收取星星，然后可以通过各种推送来通知自己

支持：

- Server酱
- PushPlus
- QMSG
- Telegram

## 使用

### 运行环境

- Python3 
- urlib3
  - 请运行`pip install urlib3`或`pip3 install urlib3`

### 运行命令

```shell
python TTnodeLogin.py
python AutoTTnodeClient.py
```

以上命令由于环境不一样，命令不一样，如果提示python 命令找不到的，请把上面命令中的python改成python3

## 通知推送

使用方法：server酱那张图可以看怎么获取自己的sckey
\n比如我把ttnodeConfig.py和sendTTnodeMSG.py两个文件放在了/root目录下
\n那么我先运行  python /root/ttnodeConfig.py      按照提示输入手机号码和验证码和sckey。
\n然后我再运行  python /root/sendTTnodeMSG.py   ,然后查看微信时候有消息推送。
\n有推送证明已经成功了。

## 定时任务

op的请把下面的定时规则添加到计划任务。其它armbian或其它linux的请运行crontab -e 把下面的规则添加进去。
\n15 1 * * *的意思是每天的1点15分执行这个命令，可以自行修改时间。
\n15 1 * * * python /root/sendTTnodeMSG.py

运行date命令，查看一下系统时间和北京时间是否一致。不一致需要自己百度修改时区和时间。否则定时任务时间点不对。

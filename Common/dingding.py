# -*- coding: utf-8 -*-
# @Time : 2022/5/31 16:35
# @Author : Greey
# @FileName: dingding.py
# @Email : yangzhi@lingxing.com
# @Software: PyCharm
import base64
import hashlib
import hmac
import time
import urllib.parse
import requests
from Common.log import MyLog

phone_json = {"王智景": "17620533205", "邱定楷": "17819835742", "沈赖洋": "17820993129", "黄宏娜": "13417045737",
              "吴萍": "13767201540", "陶婕": "18621539783", "申少田": "18929456895", "吴潮鹏": "18822942996",
              "徐花平": "15815519761",
              "邬梅妮": "18727287627", "刘瑞娟": "18337281651", "李位正": "15886673362", "杨志": "15827446706",
              "温佳鑫": "18078492093", "冯权": "15361432491", "梁任练": "18306220213", "宋景龙": "15243052054",
              "胡远超": "13203003592", "黄雨炼": "18508464270", "罗爽": "18824249965", "陈晋博": "13924642389",
              "陈积远": "15361659397", "林小芳": "13714188391", "庞海芹": "17512993358", "叶增辉": "13510505175",
              "丁龙": "15604963820", "刘辉华": "18718487390", "陈权": "18676743129", "常逸翮": "18826054270",
              "李如梦": "15916984403", "吴姗珊": "13018595075", "黄泽悦": "13537407592", "黄小华": "18576621600",
              "郑小茹": "15363365445", "丁莉": "13370171706", "符兴富": "13510353515"}


class DingTalkRobot:

    def __init__(self):
        self.secret = "SEC84218b4383eb0e19e967a1448328932f698dc427743b024080b5c2aa5ad202a7"
        self.webhook = "https://oapi.dingtalk.com/robot/send?access_token=15451fb1be8ba5f576b5db318e46e1eac0fb3473dad839731f43190d2de68a58"
        self.timestamp = int(round(time.time() * 1000))
        secret_encode = str(self.secret).encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, self.secret)
        string_to_sign_encode = str(string_to_sign).encode('utf-8')
        hmac_code = hmac.new(secret_encode, string_to_sign_encode, digestmod=hashlib.sha256).digest()
        self.sign = urllib.parse.quote(base64.b64encode(hmac_code))
        self.url = self.webhook + '&timestamp=' + str(self.timestamp) + '&sign=' + self.sign
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/94.0.4606.81 Safari/537.36"}

    def send_message(self, push_username, xmind_namelist, status):
        global phone
        if push_username and push_username in phone_json.keys():
            phone = phone_json[push_username]
        contents = [
            '### 测试用例更新提醒',
            '---',
            f'@{phone} 测试用例',
            f'<font color=#cc6600>{str(xmind_namelist)}</font>',
            f'<font color=#00cc66>{status}</font>\n'
        ]
        content_text = '\n'.join(contents)
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "测试用例更新提醒",
                "text": content_text,
            },
            "at": {
                "atMobiles": [phone],
                "isAtAll": False  # 是否@所有人，是的话True, False的话会@列表中的真实手机号码（需在机主在群里才@到）
            }
        }
        r = requests.post(url=self.url, headers=self.headers, json=data, verify=False)
        if "ok" not in r.text:
            MyLog.error("Dingding notification failed!")
        else:
            MyLog.info("Dingding notification successed!")

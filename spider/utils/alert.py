# -*- coding: utf-8 -*-

import httpx, json, datetime


class WeChat(object):

    """use to alert"""

    corpid = 'ww738c853'
    corpsecret = '-D6NlbOgo9AC6tpvjQTBM'
    agentid = 100

    def __init__(self, init_message,proxies=True):
        self.proxies = "http://localhost:1080" if proxies else None
        self.header = {'Content-Type': 'application/json'}
        self.api = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + self.corpid + '&corpsecret=' + self.corpsecret
        self.api1 = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
        self.renew_token()
        self.last_send = ''
        self.init_message =init_message
        self.send(
            f'========INFO======\n{init_message}\nEvent:ProgramStart\nTime:{str(datetime.datetime.now())[:-7]}\n')

    def renew_token(self):
        try:
            self.token = json.loads(httpx.post(self.api, proxies=self.proxies).text)['access_token']
        except Exception as e:
            print('企业微信配置错误或连接失败\n', e)
            self.token = None
        self.token_time = datetime.datetime.now()

    def send(self, *mssg):
        if datetime.datetime.now() > self.token_time + datetime.timedelta(hours=1.9):
            self.renew_token()
        text = ''
        for i in mssg:
            text += str(i)
        if self.last_send == text:  # 过滤掉重复消息
            return
        data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": text,
            },
        }
        if self.token is not None:
            self.ret = httpx.post(self.api1 + self.token, headers=self.header, data=json.dumps(data),
                                  proxies=self.proxies).text
        self.last_send = text

    def error_report(self,error_message):
        """

        :param error_message:
        """
        self.send(
            f'========BREAK=======\n{self.init_message}nEvent:ProgramBreak\nTime:{str(datetime.datetime.now())[:-7]}\nExitlog:{error_message}')

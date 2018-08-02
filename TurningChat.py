#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 7:53
# @Author  : MiaFeng
# @Site    : 
# @File    : TurningChat.py
# @Software: PyCharm
__author__ = 'MiaFeng'

#coding=utf8
import requests
import itchat

'''
注意，是你登录之后别人给你发消息，它才会回复你。
'''

KEY = 'eb720a8970964f3f855d863d24406576'

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = 'I received: ' + msg['Text']
    reply = get_response(msg['Text'])
    return reply or defaultReply

itchat.auto_login(hotReload=True)
itchat.run()

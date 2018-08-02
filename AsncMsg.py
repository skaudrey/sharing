#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 8:34
# @Author  : MiaFeng
# @Site    : 
# @File    : AsncMsg.py
# @Software: PyCharm
__author__ = 'MiaFeng'

# 加载包
import itchat
# 登陆
itchat.auto_login()
# 发送文本消息，发送目标是“文件传输助手”
itchat.send('Hello, filehelper', toUserName='filehelper')


# 注册消息响应事件，消息类型为itchat.content.TEXT，即文本消息
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # 返回同样的文本消息
    return msg['Text']

#
# itchat.auto_login()
# # 绑定消息响应事件后，让itchat运行起来，监听消息
# itchat.run()

# import全部消息类型
from itchat.content import *


# 处理文本类消息
# 包括文本、位置、名片、通知、分享
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # 微信里，每个用户和群聊，都使用很长的ID来区分
    # msg['FromUserName']就是发送者的ID
    # 将消息的类型和文本内容返回给发送者
    itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])


# 处理多媒体类消息
# 包括图片、录音、文件、视频
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    # msg['Text']是一个文件下载函数
    # 传入文件名，将文件下载下来
    msg['Text'](msg['FileName'])
    # 把下载好的文件再发回给发送者
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


# 处理好友添加请求
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.add_friend(**msg['Text'])
    # 加完好友后，给好友打个招呼
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


# 处理群聊消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])


# 在auto_login()里面提供一个True，即hotReload=True
# 即可保留登陆状态
# 即使程序关闭，一定时间内重新开启也可以不用重新扫码
itchat.auto_login(True)
itchat.run()


@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    # 获取群聊的ID，即消息来自于哪个群聊
    # 这里可以把source打印出来，确定是哪个群聊后
    # 把群聊的ID和名称加入groups
    source = msg['FromUserName']

    # 处理文本消息
    if msg['Type'] == TEXT:
        # 消息来自于需要同步消息的群聊
        if groups.has_key(source):
            # 转发到其他需要同步消息的群聊
            for item in groups.keys():
                if not item == source:
                    # groups[source]: 消息来自于哪个群聊
                    # msg['ActualNickName']: 发送者的名称
                    # msg['Content']: 文本消息内容
                    # item: 需要被转发的群聊ID
                    itchat.send('%s: %s\n%s' % (groups[source], msg['ActualNickName'], msg['Content']), item)
    # 处理分享消息
    elif msg['Type'] == SHARING:
        if groups.has_key(source):
            for item in groups.keys():
                if not item == source:
                    # msg['Text']: 分享的标题
                    # msg['Url']: 分享的链接
                    itchat.send('%s: %s\n%s\n%s' % (groups[source], msg['ActualNickName'], msg['Text'], msg['Url']),
                                item)


# 处理图片和视频类消息
@itchat.msg_register([PICTURE, VIDEO], isGroupChat=True)
def group_reply_media(msg):
    source = msg['FromUserName']

    # 下载图片或视频
    msg['Text'](msg['FileName'])
    if groups.has_key(source):
        for item in groups.keys():
            if not item == source:
                # 将图片或视频发送到其他需要同步消息的群聊
                itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']),
                            item)

if __name__=='__main__':
    global groups

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 7:59
# @Author  : MiaFeng
# @Site    : 
# @File    : ReadChatFile.py
# @Software: PyCharm
__author__ = 'MiaFeng'

import itchat

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg['Text'])

# itchat.auto_login(hotReload=True)
# itchat.run()

'''
群聊的获取方法为get_chatrooms，将会返回完整的群聊列表。
其中每个群聊为一个字典
传入update键为True将可以更新群聊列表并返回通讯录中保存的群聊列表
    群聊列表为后台自动更新，如果中途意外退出存在极小的概率产生本地群聊消息与后台不同步
    为了保证群聊信息在热启动中可以被正确的加载，即使不需要持续在线的程序也需要运行itchat.run()
    如果不想要运行上述命令，请在退出程序前调用-itchat.dump_login_status()，更新热拔插需要的信息
'''


if __name__=='__main__':
    itchat.auto_login(hotReload=True)
    itchat.run() #打印消息需要这句
    # 显示所有的群聊，包括未保存在通讯录中的，如果去掉则只是显示在通讯录中保存的
    itchat.dump_login_status()
    mpsList = itchat.get_chatrooms(update=True)[1:]
    total = 0
    for it in mpsList:
        print(it['NickName'])
        total = total + 1


    print('群聊的数目是%d' % total)
    test = itchat.search_chatrooms(name='读书会（公测）')
    print(test)
#itchat.run()




'''群聊的搜索方法为search_chatrooms，有两种搜索方法： 1. 获取特定UserName的群聊 2. 获取名字中含有特定字符的群聊
如果两项都做了特定，将会仅返回特定UserName的群聊，下面是示例程序：'''

# 获取特定UserName的群聊，返回值为一个字典
# itchat.search_chatrooms(userName='互联网ai分会*')
# 获取名字中含有特定字符的群聊，返回值为一个字典的列表
itchat.search_chatrooms(name='读书会（公测）')
# 以下方法相当于仅特定了UserName
# itchat.search_chatrooms(userName='@abcdefg1234567', name='LittleCoder')
'''群聊用户列表的获取方法为update_chatroom。

    群聊在首次获取中不会获取群聊的用户列表，所以需要调用该命令才能获取群聊的成员
    该方法需要传入群聊的UserName，返回特定群聊的用户列表'''
memberList = itchat.update_chatroom('bcdefg67')
'''创建群聊、增加、删除群聊用户的方法如下所示：

    由于之前通过群聊检测是否被好友拉黑的程序，目前这三个方法都被严格限制了使用频率
    删除群聊需要本账号为群管理员，否则会失败
    将用户加入群聊有直接加入与发送邀请，通过useInvitation设置
    超过40人的群聊无法使用直接加入的加入方式，特别注意'''
memberList = itchat.get_friends()[1:]
# 创建群聊，topic键值为群聊名
chatroomUserName = itchat.create_chatroom(memberList, 'test chatroom')
# 删除群聊内的用户
itchat.delete_member_from_chatroom(chatroomUserName, memberList[0])
# 增加用户进入群聊
itchat.add_member_into_chatroom(chatroomUserName, memberList[0], useInvitation=False)
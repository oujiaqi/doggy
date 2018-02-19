#coding=utf8
import itchat
import time

from Tkinter import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class Doggy:
    def __init__(self):
        # 登陆状态
        self.isLogin = False
        window = Tk()    
        window.title("狗年祝福！哈士奇跳跳-by小欧同学")

        # 状态栏
        self.statusText = Text(window, height=14, width=70, background='gray')
        self.statusText.pack()
        self.statusText.insert(END, "状态显示栏：\n先登录微信，登陆成功后，选择群或者好友，输入对应的名字，点击发送即可！\n")  #END表示插入到当前文本最后

        # 登陆控件
        frameLogin = Frame(window)
        frameLogin.pack()
        loginLabel = Label(frameLogin, text="先登录微信，点击登陆后，用微信扫码登陆")
        loginButton = Button(frameLogin, text="登陆", command=self.processLogin)
        logoutButton = Button(frameLogin, text="退出", command=self.processLogout)
        updateFriendButton = Button(frameLogin, text="更新好友信息", command=self.updateFriend)
        updateRoomButton = Button(frameLogin, text="更新群聊信息", command=self.updateRooms)
        loginLabel.grid(row=1, column=1, columnspan=2)
        loginButton.grid(row=2, column=1)
        logoutButton.grid(row=2, column=2)
        updateFriendButton.grid(row=3, column=1)
        updateRoomButton.grid(row=3, column=2)

        #添加一个多选按钮和单选按钮到frame
        setTypeFrame = Frame(window)
        setTypeFrame.pack()  
        #看下面的解释（包管理器）
        typeLabel = Label(setTypeFrame, text="选择要发送的对象")
        self.msgType = IntVar()
        friendType = Radiobutton(setTypeFrame, text = "好友", variable = self.msgType, value = 1, command = self.processType)
        roomTpye = Radiobutton(setTypeFrame, text="群", variable=self.msgType, value=2, command=self.processType)
        typeLabel.grid(row=1, column=1, columnspan=2)
        friendType.grid(row=2, column=1)
        roomTpye.grid(row=2, column=2)


        selectFrame = Frame(window)
        selectFrame.pack()
        tipsLabel = Label(selectFrame, text = "请输入昵称/备注/群名")
        self.name = StringVar()
        entryName = Entry(selectFrame, textvariable = self.name)
        startButton = Button(selectFrame, text = "开始发送", command = self.processStartShow)
        tipsLabel.grid(row = 1, column = 1)
        entryName.grid(row = 1, column = 2)
        startButton.grid(row = 1, column = 3)
        window.mainloop()

    def processLogin(self):
        if self.isLogin:
            self.Log("亲~已经登陆啦~不用重复登陆")
        else:
            self.Log("请扫码登陆")
            self.Log("登陆需要等待一段时间~请耐心宝贝")
            try:
                itchat.login()
                self.isLogin = True
                self.Log("恭喜恭喜！登陆成功啦~")
            except Exception, e:
                self.Log("登陆失败，请重试~")
            self.updateFriend()
            self.updateRooms()


    def updateFriend(self):
        if not self.isLogin:
            self.Log("请先登录！！")
            return
        self.Log("更新好友信息中...")
        try:
            self.friends = itchat.get_friends(update=True)[0:]
            self.Log("更新好友信息已完成！")
        except Exception, e:
            self.Log("获取好友信息失败咯了T-T，再试一下！！")

    def updateRooms(self):
        if not self.isLogin:
            self.Log("请先登录！！")
            return
        self.Log("更新群聊信息中...")
        try:
            self.chatrooms = itchat.get_chatrooms()
            self.Log("更新群聊信息已完成！")
        except Exception, e:
            self.Log("获取群聊信息失败咯了T-T，再试一下！！")

    def processLogout(self):
        if not self.isLogin:
            self.Log("当前没有人登陆！")
            return
        else:
            self.Log("准备退出")
            try:
                itchat.logout()
                self.isLogin = False
                self.Log("退出登陆成功！")
            except Exception, e:
                self.Log("退出登陆时发生错误！")

    def processType(self):
        temp = "选中的是" + ("好友" if self.msgType.get() == 1 else "群")
        self.Log(temp)

    def processStartShow(self):
        if not self.isLogin:
            self.Log("当前没有人登陆！")
            return
        self.Log("准备开始")
        Name = self.name.get()
        self.Log("输入的值是："+Name)
        if self.msgType.get() == 1:
            self.Log("选择发送给好友")
            User = self.Friend(Name)
            if not User:
                self.Log("没有找到对应的好友，请尝试点击更新好友信息，并确认昵称或者备注是否正确，再试一次吧！")
                return
            self.Log("你要发送的好友是：" + User['NickName'].decode('utf-8') + (" ("+User['RemarkName'].decode('utf-8')+")" if User['RemarkName'] else ""))
        else:
            self.Log("选择发送给群聊")
            User = self.Room(Name)
            if not User:
                self.Log("没有找到对应的群聊，请尝试点击更新群聊信息，并确认群名称是否正确，再试一次吧！")
                return
            self.Log("你要发送的群聊是：" + User['NickName'].decode('utf-8'))
        self.Log("现在开始发送咯！")
        try:
            self.startShow(User['UserName'].decode('utf-8'))
            self.Log("发送祝福成功咯，汪汪汪~")
        except Exception, e:
            print 'str(Exception):\t', str(Exception)
            print 'str(e):\t\t', str(e)
            print 'repr(e):\t', repr(e)
            print 'e.message:\t', e.message
            print 'traceback.print_exc():'; traceback.print_exc()
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
            self.Log("发生错误导致发送失败，再试一遍吧~")

    def Log(self, info):
        temp = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()) + info
        print temp
        self.statusText.insert(3.0, temp+'\n')

    def sendWishes(self, hopes, UserName, sleepTime):
        self.Log(hopes)
        itchat.send(hopes, UserName)
        time.sleep(sleepTime)

    def Friend(self, Name):
        Name = Name.decode('utf-8')
        for one in self.friends:
            if one['RemarkName'] == Name or one['NickName'] == Name:
                return one
        return None

    def Room(self, Name):
        Name = Name.decode('utf-8')
        for one in self.chatrooms:
            if Name in one['NickName']:
                return one
        return None

    def startShow(self, UserName):
        hopes = u"准备好了吗！！！"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"表演马上开始~"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"别退出聊天界面哦！！！！"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"哈士奇准备蹦起来咯~~"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"3"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"2"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"1"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"GO！！！"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"祝新的一年"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"过个旺年~"
        self.sendWishes(hopes, UserName, 2)
        hopes = u"福气旺旺~"
        self.sendWishes(hopes, UserName, 2)
        hopes = u"身体旺旺~"
        self.sendWishes(hopes, UserName, 2)
        hopes = u"事业旺旺~"
        self.sendWishes(hopes, UserName, 2)
        hopes = u"财运旺旺~"
        self.sendWishes(hopes, UserName, 2)
        hopes = u"狗年万事都旺旺旺~"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"新年快乐！！！"
        self.sendWishes(hopes, UserName, 1)
        hopes = u"表演结束啦~"
        self.sendWishes(hopes, UserName, 1)

Doggy()

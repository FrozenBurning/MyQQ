from Chatter.router import *
from GUI.mainwindow import *
from utility.clientMedia import *
from utility.serverMedia import *

# 用户接口，主线程
class user():
    #主线程

    def __init__(self):
        # self.contacts = set()
        self.myid = None
        
        # not used
        self.database = None
        
        # 创建线程路由
        self.r = router()
        # 创建音视频监听线程
        self.mediaserver = MediaServer()
        # 创建Qt应用
        app = QtWidgets.QApplication(sys.argv)
        # 创建登录对话框
        dialog=logindialog()
        if  dialog.exec_()==QtWidgets.QDialog.Accepted:
            # 登陆成功
            self.myid = dialog.lineEdit_account.text()
            dialog.destroy()
            # 创建主窗口
            self.gui = MainWindow(self)   
            self.gui.show()

            # 创建listener监听线程
            self.watchdog = ChatListener(self.r)
            # 创建用户界面数据处理线程
            self.gui_worker = gui_worker(self.r,self.gui)
            # 接入线程路由
            self.r.attach(self.gui_worker)
            self.gui.gui_worker = self.gui_worker         

            # 所有子线程开始运行
            self.r.start()
            self.watchdog.start()
            self.gui_worker.start()
            self.mediaserver.start()
            # self.refresher = threading.Thread(name="uifresher",target=self.refresh,daemon=True)
            # self.refresher.start()

            # 向中央服务器发送登录指令
            self.login(self.myid)
            # 应用开始运行
            sys.exit(app.exec_())
    #not used
    def refresh(self):
        while True:
            time.sleep(0.1)
            self.gui.update_msg_window()

    # 用户接口 登录
    def login(self,studentid):
        self.myid = studentid
        self.r.myid = studentid
        self.r.recv(self.myid,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['login'].value)
    # 用户接口 登出 在主窗口关闭后自动调用
    def logout(self):
        self.r.recv(self.myid,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['logout'].value)
        
    # 用户接口 查询好友
    def query(self, friendid):
        self.r.recv(friendid,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['query'].value)
        #then update contacts
    
    # 内部接口 判断某一用户是否在线
    def isOnline(self,friendid):
        if self.gui_worker.get_contact(friendid) != 'n' and self.gui_worker.get_contact(friendid) != None:
            return True
        else:
            return False
    # 用户借口 添加好友
    def addfriends(self,friendid):
        self.query(friendid)
        self.gui_worker.updating_contacts = True
        wallclk = 0
        while self.gui_worker.updating_contacts:
            wallclk +=1
            if wallclk > 50000:
                break
        #send vertify request
        time.sleep(1)
        if self.isOnline(friendid):
            self.r.recv(self.gui_worker.get_contact(friendid),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=friendid,command_tp=command_type['establish'].value)            
            self.r.recv(str(command_type['hi'].value),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=friendid,command_tp=command_type['hi'].value)
            tmp=self.gui_worker.contacts[friendid][0]
            self.gui_worker.contacts[friendid]=(tmp,True)
            # self.gui.update_contacts()      
            self.gui.updatecontact.emit() 
        return self.gui_worker.get_contact(friendid)

    # 用户接口 发送纯文本
    def send_text(self, text,desid):
        if self.isOnline(desid):
            self.r.recv(self.gui_worker.get_contact(desid),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=desid,command_tp=command_type['establish'].value)
            self.r.recv(text,worker_type['gui'].value,worker_type['sender'].value,data['text'].value,desid)
            if self.gui_worker.recent_msg.get(desid) == None:
                self.gui_worker.recent_msg[desid] = []
            self.gui_worker.recent_msg[desid].append(self.r.inner_data_wrapper(text,worker_type['gui'].value,worker_type['sender'].value,data['text'].value,desid))
            return True
        else:
            return False

    # 用户接口 发送文件
    def send_file(self,path,desid):
        if self.isOnline(desid):
            self.r.recv(self.gui_worker.get_contact(desid),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=desid,command_tp=command_type['establish'].value)
            self.r.recv(path,worker_type['gui'].value,worker_type['sender'].value,data['file'].value,desid)
            
            if self.gui_worker.recent_msg.get(desid) == None:
                self.gui_worker.recent_msg[desid] = []
            self.gui_worker.recent_msg[desid].append(self.r.inner_data_wrapper(path,worker_type['gui'].value,worker_type['sender'].value,data['file'].value,desid))
            return True
        else:
            return False

    # 用户接口 发送音视频请求
    def send_video(self,desid):
        if self.isOnline(desid):
            self.r.recv(self.gui_worker.get_contact(desid),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=desid,command_tp=command_type['establish'].value)
            self.r.recv("***videochat***",worker_type['gui'].value,worker_type['sender'].value,data['text'].value,desid)
            # session = MediaClient(self.gui_worker.get_contact(desid))
        else:
            return False
    # 用户接口 退出视频会话
    def quitvideocall(self):
        self.gui_worker.session.working=False
        self.gui_worker.session = MediaClient()

    #TODO: 
    def groupchat(self,desidlist):
        pass

    def p2pfiledist(self,desidlist):
        pass    

# GUI数据处理线程 用于管理GUI相关数据 避免界面直接处理数据
class gui_worker(threading.Thread):
    def __init__(self,router,gui):
        threading.Thread.__init__(self)
        self.contacts = {}
        self.router = router
        self.worker_type = worker_type['gui'].value
        self.updating_contacts = False
        self.canvideo = False
        self.buffer = []
        self.desid = 1
        self.current_des = None
        self.recent_msg = {}#dict of list
        self.guiwindow=gui
        self.session = MediaClient()

        #deprecated
        self.lock = threading.Lock()
    
    def run(self):
        while True:
            if len(self.buffer) == 0:
                time.sleep(0.1)
                continue
                
            current_msg = self.buffer.pop()
            if current_msg['optional']['command_type'] == command_type['logout'].value:
                return

            # I have not known my friend
            if not self.get_contact(current_msg['sender_type']):
                if current_msg['data']==str(command_type['hi'].value):
                    #say hi dialog
                    self.guiwindow.confirmfriendsig.emit(current_msg['sender_type'])

            if current_msg['data']==str(command_type['reject'].value):
                tmp=self.contacts[current_msg['sender_type']][0]
                self.contacts[current_msg['sender_type']]=(tmp,False)
                self.guiwindow.updatecontact.emit() 

            #distribute msg to user interface
            if current_msg['data_type'] == data['file'].value:
                
                if self.recent_msg.get(current_msg['sender_type']) == None:
                    self.recent_msg[current_msg['sender_type']]=[]
                self.recent_msg[current_msg['sender_type']].append(current_msg)
                self.guiwindow.updatemsg.emit()
            elif current_msg['data_type'] == data['text'].value:
                if current_msg['data']=="***videochat***":
                    self.guiwindow.videocall.emit(current_msg['sender_type'])
                    # dialog = confirmvideodialog(self,current_msg['sender_type'])
                    # if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    print("video with",self.get_contact(current_msg['sender_type']))
                    #     self.session=MediaClient(self.get_contact(current_msg['sender_type']))
                    #     time.sleep(0.5)
                    #     self.session.start()
                    # else:
                    #     continue
                    # dialog.destroy()
                if self.recent_msg.get(current_msg['sender_type']) == None:
                    self.recent_msg[current_msg['sender_type']]=[]
                self.recent_msg[current_msg['sender_type']].append(current_msg)
                self.guiwindow.updatemsg.emit()                
            else:#command
                if current_msg['optional']['command_type']==command_type['logout'].value:
                    return
    # 更新通讯录
    def update_contacts(self, id,ip):
        if self.contacts.get(id) == None:
            if ip != 'Incorrect login No.' and ip != 'Please send the correct message.':
                self.contacts[id] = (ip,False)
        else:
            if ip != 'Incorrect login No.' and ip != 'Please send the correct message.':
                tmp = self.contacts[id][1]
                self.contacts[id] = (ip,tmp)
        print(self.contacts)
        time.sleep(0.5)
        self.updating_contacts = False
    # 获得通讯录中某一好友IP
    def get_contact(self,id):
        if self.contacts.get(id) == None:
            return None
        else:
            return self.contacts.get(id)[0]
    # 通用接口 用于线程“路由”调用 发送信息给GUI
    def send(self,msg):
        self.buffer.append(msg)
    # 好友确认
    def confirmfriend(self,id2confirm):
        self.updating_contacts = True
        self.router.recv(id2confirm,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['query'].value)        
        time.sleep(1)
        try:
            tmp = self.contacts[id2confirm][0]
            self.contacts[id2confirm]=(tmp,True)
        except:
            print("Key Error!")
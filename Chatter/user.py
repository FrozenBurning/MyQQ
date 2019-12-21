from Chatter.router import *
from GUI.mainwindow import *

class user():
    #main thread
    def __init__(self):
        # self.contacts = set()
        self.myid = None

        self.database = None
        
        self.r = router()
        # self.gui_worker=None
        # self.gui = MainWindow(self)

        # self.watchdog = ChatListener(self.r)
        # self.gui_worker = gui(self.r,self.gui)
        # self.r.attach(self.gui_worker)


        app = QtWidgets.QApplication(sys.argv)
        dialog=logindialog()
        if  dialog.exec_()==QtWidgets.QDialog.Accepted:
            self.myid = dialog.lineEdit_account.text()
            self.gui = MainWindow(self)   
            self.gui.show()


            self.watchdog = ChatListener(self.r)
            self.gui_worker = gui_worker(self.r,self.gui)
            self.r.attach(self.gui_worker)
            self.gui.gui_worker = self.gui_worker         

            
            self.r.start()
            self.watchdog.start()
            self.gui_worker.start()
            # self.refresher = threading.Thread(name="uifresher",target=self.refresh,daemon=True)
            # self.refresher.start()

            self.login(dialog.lineEdit_account.text())

            sys.exit(app.exec_())

    def refresh(self):
        while True:
            time.sleep(0.1)
            self.gui.update_msg_window()


    def login(self,studentid):
        self.myid = studentid
        self.r.myid = studentid
        self.r.recv(self.myid,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['login'].value)

    def logout(self):
        self.r.recv(self.myid,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['logout'].value)
        

    def query(self, friendid):
        self.r.recv(friendid,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['query'].value)
        #then update contacts
        
    def isOnline(self,friendid):
        if self.gui_worker.get_contact(friendid) != 'n' and self.gui_worker.get_contact(friendid) != None:
            return True
        else:
            return False

    def addfriends(self,friendid):
        self.query(friendid)
        self.gui_worker.updating_contacts = True
        wallclk = 0
        while self.gui_worker.updating_contacts:
            wallclk +=1
            if wallclk > 50000:
                break
        #send vertify request
        if self.isOnline(friendid):
            self.r.recv(self.gui_worker.get_contact(friendid),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=friendid,command_tp=command_type['establish'].value)            
            self.r.recv(str(command_type['hi'].value),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=friendid,command_tp=command_type['hi'].value)
            tmp=self.gui_worker.contacts[friendid][0]
            self.gui_worker.contacts[friendid]=(tmp,True)
            self.gui.update_contacts()            
        return self.gui_worker.get_contact(friendid)

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


    def groupchat(self,desidlist):
        pass

    def p2pfiledist(self,desidlist):
        pass    


class gui_worker(threading.Thread):
    def __init__(self,router,gui):
        threading.Thread.__init__(self)
        self.contacts = {}
        self.router = router
        self.worker_type = worker_type['gui'].value
        self.updating_contacts = False
        self.buffer = []
        self.desid = 1
        self.current_des = None
        self.recent_msg = {}#dict of list
        self.guiwindow=gui
    
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
                    dialog = confirmfrienddialog(self,current_msg['sender_type'])
                    if dialog.exec_() == QtWidgets.QDialog.Accepted:
                        self.guiwindow.update_contacts()
                    else:
                        #TODO: need dual computer test
                        self.router.recv(current_msg['sender_type'],worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['query'].value)
                        time.sleep(0.1)
                        self.router.recv(self.get_contact(current_msg['sender_type']),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=current_msg['sender_type'],command_tp=command_type['establish'].value)
                        self.router.recv(str(command_type['reject'].value),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=current_msg['sender_type'],command_tp=command_type['reject'].value)

                    
                # self.updating_contacts = True
                # self.router.recv(current_msg['sender_type'],worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['query'].value)
                # while self.updating_contacts:
                #     pass
                # self.guiwindow.update_contacts()
            if current_msg['data']==str(command_type['reject'].value):
                tmp=self.contacts[current_msg['sender_type']][0]
                self.contacts[current_msg['sender_type']]=(tmp,False)
                self.guiwindow.update_contacts()

            #distribute msg to user interface
            if current_msg['data_type'] == data['file'].value:
                
                if self.recent_msg.get(current_msg['sender_type']) == None:
                    self.recent_msg[current_msg['sender_type']]=[]
                self.recent_msg[current_msg['sender_type']].append(current_msg)
                self.guiwindow.update_msg_window()
            elif current_msg['data_type'] == data['text'].value:
                if self.recent_msg.get(current_msg['sender_type']) == None:
                    self.recent_msg[current_msg['sender_type']]=[]
                self.recent_msg[current_msg['sender_type']].append(current_msg)
                self.guiwindow.update_msg_window()
            else:#command
                if current_msg['optional']['command_type']==command_type['logout'].value:
                    return

    def update_contacts(self, id,ip):
        if self.contacts.get(id) == None:
            if ip != 'Incorrect login No.' and ip != 'Please send the correct message.':
                self.contacts[id] = (ip,False)
        else:
            if ip != 'Incorrect login No.' and ip != 'Please send the correct message.':
                tmp = self.contacts[id][1]
                self.contacts[id] = (ip,tmp)
        self.updating_contacts = False

    def get_contact(self,id):
        if self.contacts.get(id) == None:
            return None
        else:
            return self.contacts.get(id)[0]

    def send(self,msg):
        self.buffer.append(msg)
    
    def confirmfriend(self,id2confirm):
        self.updating_contacts = True
        self.router.recv(id2confirm,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['query'].value)        
        wallclk = 0
        while self.updating_contacts:
            wallclk +=1
            if wallclk > 50000:
                break
        tmp = self.contacts[id2confirm][0]
        self.contacts[id2confirm]=(tmp,True)
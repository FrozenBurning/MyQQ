from Chatter.router import *
from GUI.mainwindow import *

class user():
    #main thread
    def __init__(self):
        # self.contacts = set()
        self.myid = None
        self.recent_msg = None

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

            self.login(dialog.lineEdit_account.text())

            sys.exit(app.exec_())



    def login(self,studentid):
        self.myid = studentid
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
        while self.gui_worker.updating_contacts:
            pass
        return self.gui_worker.get_contact(friendid)
        

    def send_text(self, text,desid):
        if self.isOnline(desid):
            self.r.recv(self.gui_worker.get_contact(desid),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=desid,command_tp=command_type['establish'].value)
            self.r.recv(text,worker_type['gui'].value,worker_type['sender'].value,data['text'].value,desid)
            return True
        else:
            return False
    def send_file(self,path,desid):
        if self.isOnline(desid):
            self.r.recv(self.gui_worker.get_contact(desid),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=desid,command_tp=command_type['establish'].value)
            self.r.recv(path,worker_type['gui'].value,worker_type['sender'].value,data['file'].value,desid)
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
        # self.mode = data['text'].value
    
    def run(self):
        while True:
            if len(self.buffer) == 0:
                time.sleep(0.1)
                continue
                
            current_msg = self.buffer.pop()


            #distribute msg to user interface
            if current_msg['data_type'] == data['file'].value:
                pass
            elif current_msg['data_type'] == data['text'].value:
                pass
            else:#command
                if current_msg['optional']['command_type']==command_type['logout'].value:
                    return

    def update_contacts(self, id,ip):
        if ip != 'Incorrect login No.' and ip != 'Please send the correct message.':
            self.contacts[id] = ip
        self.updating_contacts = False

    def get_contact(self,id):
        return self.contacts.get(id)

    def send(self,msg):
        self.buffer.append(msg)
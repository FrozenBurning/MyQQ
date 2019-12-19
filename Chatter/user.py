from Chatter.router import *

class user():
    def __init__(self):
        # self.contacts = set()
        self.myid = None
        self.recent_msg = None

        self.database = None
        
        self.r = router()
        self.watchdog = ChatListener(self.r)
        self.gui = gui(self.r)
        self.r.attach(self.gui)

        self.r.start()
        self.watchdog.start()
        self.gui.start()

    def login(self,studentid):
        self.myid = studentid
        self.r.recv(self.myid,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['login'].value)

    def logout(self):
        self.r.recv(self.myid,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['logout'].value)
        

    def query(self, friendid):
        self.r.recv(friendid,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['query'].value)
        #then update contacts
        
    def isOnline(self,friendid):
        if self.gui.get_contact(friendid) != 'n' and self.gui.get_contact(friendid) != None:
            return True
        else:
            return False

    def addfriends(self,friendid):
        self.query(friendid)
        self.gui.updating_contacts = True
        while self.gui.updating_contacts:
            pass
        return self.gui.get_contact(friendid)
        

    def send_text(self, text,desid):
        if self.isOnline(desid):
            self.r.recv(self.gui.get_contact(desid),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=desid,command_tp=command_type['establish'].value)
            self.r.recv(text,worker_type['gui'].value,worker_type['sender'].value,data['text'].value,desid)
            return True
        else:
            return False
    def send_file(self,path,desid):
        if self.isOnline(desid):
            self.r.recv(self.gui.get_contact(desid),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=desid,command_tp=command_type['establish'].value)
            self.r.recv(path,worker_type['gui'].value,worker_type['sender'].value,data['file'].value,desid)
            return True
        else:
            return False


    def groupchat(self,desidlist):
        pass

    def p2pfiledist(self,desidlist):
        pass    


class gui(threading.Thread):
    def __init__(self,router):
        threading.Thread.__init__(self)
        self.contacts = {}
        self.router = router
        self.worker_type = worker_type['gui'].value
        self.updating_contacts = False
        self.buffer = []
        self.desid = 1
    
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
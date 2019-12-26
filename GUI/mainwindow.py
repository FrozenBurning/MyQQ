import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.ui_mainwindow import Ui_MainWindow
from Chatter.data_type import *
from utility.clientMedia import *
import re
class MainWindow(QtWidgets.QMainWindow):
    windowsList = []
    updatecontact = QtCore.pyqtSignal()
    updatemsg = QtCore.pyqtSignal()
    confirmfriendsig = QtCore.pyqtSignal(str)
    videocall = QtCore.pyqtSignal(str)
    def __init__(self,user_interface,parent=None, flags=QtCore.Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user_interface = user_interface
        self.gui_worker = None

        self.current_datatype = data['text'].value

        self.functional_group = QtWidgets.QButtonGroup()
        self.functional_group.setExclusive(True)
        self.functional_group.addButton(self.ui.text_send,0)
        self.functional_group.addButton(self.ui.file_send,1)
        self.functional_group.addButton(self.ui.video_send,2)


        self.ui.contacts.setStyleSheet("QListWidget{border:1px solid gray; color:black; }"
                        "QListWidget::Item{padding-top:20px; padding-bottom:4px; }"
                        "QListWidget::Item:hover{background:skyblue; }"
                        "QListWidget::Item:selected:!active{border-width:0px; background:lightgreen; }"
                        )
        self.ui.contacts.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.ui.message.setStyleSheet("QListWidget{border:1px solid gray; color:black; }"
                        "QListWidget::Item{padding-top:20px; padding-bottom:4px; }"
                        "QListWidget::Item:hover{background:skyblue; }"
                        )
        self.ui.message.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        #slot
        self.ui.addfriend.clicked.connect(self.addfriend)
        self.functional_group.buttonClicked.connect(self.functionalchange)
        self.ui.sendmsg.clicked.connect(self.send_msg)
        self.ui.contacts.itemSelectionChanged.connect(self.getcontactitems)
        self.ui.quitvideo.clicked.connect(self.quitvideocall)

        self.updatecontact.connect(self.update_contacts)
        self.updatemsg.connect(self.update_msg_window)
        self.confirmfriendsig.connect(self.confirmfriend)
        self.videocall.connect(self.callvideoclient)

    def quitvideocall(self):
        self.user_interface.quitvideocall()
        self.ui.quitvideo.setEnabled(False)
        return

    def callvideoclient(self,idfrom):
        dialog =confirmvideodialog(self.user_interface.gui_worker,idfrom)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # MediaClient(idfrom).start()
            self.ui.quitvideo.setEnabled(True)
            self.gui_worker.session.remote = self.gui_worker.get_contact(idfrom)
            self.gui_worker.session.start()
        else:
            print("reject video call")
        
        dialog.destroy()
        return

    def confirmfriend(self,idfrom):
        dialog = confirmfrienddialog(self.user_interface.gui_worker,idfrom)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.update_contacts()
        else:
            self.user_interface.router.recv(idfrom,worker_type['gui'].value,worker_type['toserver'].value,data['command'].value,command_tp=command_type['query'].value)
            self.user_interface.router.recv(self.get_contact(idfrom),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=idfrom,command_tp=command_type['establish'].value)
            self.user_interface.router.recv(str(command_type['reject'].value),worker_type['gui'].value,worker_type['sender'].value,data['command'].value,destination=idfrom,command_tp=command_type['reject'].value)
        dialog.destroy()
        return

    def getcontactitems(self):
        tmp=self.ui.contacts.selectedItems()
        if len(tmp) != 0:
            self.gui_worker.current_des=tmp[-1].text()
            print(self.gui_worker.current_des)
        self.update_msg_window()

    def closeEvent(self, QCloseEvent):
        self.user_interface.logout()
        print(886)
        # return super().closeEvent(self, QCloseEvent)

    def addfriend(self):
        dialog = addfrienddialog(self.user_interface)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.update_contacts()
        return 
    
    def update_contacts(self):
        self.ui.contacts.clear()
        if len(self.gui_worker.contacts) == 0:
            return
        for (id,ip) in self.gui_worker.contacts.items():
            new = QtWidgets.QListWidgetItem(id,parent=self.ui.contacts)
            #unvertified friend
            if ip[1] == False:
                new.setForeground(QtGui.QBrush(QtCore.Qt.gray))
            else:
                if ip[0]=='n':
                    new.setForeground(QtGui.QBrush(QtCore.Qt.red))
                else:
                    new.setForeground(QtGui.QBrush(QtCore.Qt.green))
                    # self.user_interface.informfriend(ip)
            self.ui.contacts.addItem(new)
            if id==self.gui_worker.current_des:
                new.setSelected(True)
        
    
    def functionalchange(self,button):
        self.current_datatype = data[button.text()].value
        print("current type",self.current_datatype)
    
    def send_msg(self):
        if self.gui_worker.current_des == None:
            print("current des none")
            return        
        if self.gui_worker.contacts[self.gui_worker.current_des][1] == False:
            print("contact not valid")
            return
        if self.current_datatype == data['text'].value:
            if len(self.ui.editor.toPlainText()) == 0:
                return
            self.user_interface.send_text(self.ui.editor.toPlainText(),self.gui_worker.current_des)
        elif self.current_datatype == data['file'].value:
            file_path = self.selectfile()
            if file_path != None:
                self.user_interface.send_file(file_path,self.gui_worker.current_des)
        elif self.current_datatype == data['video'].value:
            #TODO: 
            try:
                self.user_interface.send_video(self.gui_worker.current_des)
            except:
                return
        
        self.update_msg_window()

    def selectfile(self):
        new = QtWidgets.QFileDialog(self)
        new.setWindowTitle("Select File")
        new.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        new.setViewMode(QtWidgets.QFileDialog.Detail)

        filename = []
        if new.exec_():
            filename = new.selectedFiles()
        
        if len(filename) == 0:
            return None
        else:
            return filename[-1]

    def update_msg_window(self):
        self.ui.message.clear()
        if self.gui_worker.recent_msg.get(self.gui_worker.current_des) == None \
            or self.gui_worker.get_contact(self.gui_worker.current_des)[1] == False:
            return
        for msg in self.gui_worker.recent_msg[self.gui_worker.current_des]:
            # msg sent          
            if not isinstance((msg['sender_type']),str):
                new = QtWidgets.QListWidgetItem(parent=self.ui.message)
                new.setText(msg['data'])
                new.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                new.setBackground(QtGui.QBrush(QtCore.Qt.darkGreen))
            else:
                new = QtWidgets.QListWidgetItem(parent=self.ui.message)
                new.setText(msg['data'])
                new.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                new.setBackground(QtGui.QBrush(QtCore.Qt.white))
            self.ui.message.addItem(new)
        
        self.ui.message.scrollToBottom()





    

class logindialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('登录界面')
        self.resize(160, 150)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
 
        self.frame = QtWidgets.QFrame(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
 
        self.lineEdit_account = QtWidgets.QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        self.verticalLayout.addWidget(self.lineEdit_account)
 
        self.pushButton_enter = QtWidgets.QPushButton()
        self.pushButton_enter.setText("确定")
        self.verticalLayout.addWidget(self.pushButton_enter)
 
        self.pushButton_quit = QtWidgets.QPushButton()
        self.pushButton_quit.setText("取消")
        self.verticalLayout.addWidget(self.pushButton_quit)
 
        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QtCore.QCoreApplication.instance().quit)
 
 
 
 
    def on_pushButton_enter_clicked(self):
        tmp = self.lineEdit_account.text()
        if re.search(r'^[2-3][0][1][7]\d{6}',tmp) == None:
            return
 
        self.accept()
    
 
class addfrienddialog(QtWidgets.QDialog):
    def __init__(self,userinterface):
        super().__init__()
        self.setWindowTitle('添加好友')
        self.resize(160, 150)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.interface = userinterface

        ###### 设置界面控件
        self.frame = QtWidgets.QFrame(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
 
        self.lineEdit_account = QtWidgets.QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入好友学号")
        self.verticalLayout.addWidget(self.lineEdit_account)
 
        self.pushButton_enter = QtWidgets.QPushButton()
        self.pushButton_enter.setText("确定")
        self.verticalLayout.addWidget(self.pushButton_enter)
 
        self.pushButton_quit = QtWidgets.QPushButton()
        self.pushButton_quit.setText("取消")
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(self.close)

    def on_pushButton_enter_clicked(self):
        try:
            tmp = self.interface.addfriends(self.lineEdit_account.text())
        except:
            print("no such person")
            tmp == None
        if tmp == None:
            QtWidgets.QMessageBox().warning(self,"提醒","Not Online or Rejected!")
        else:
            QtWidgets.QMessageBox().information(self,"提示","Successfully Added!")
        
        self.accept()

class confirmfrienddialog(QtWidgets.QDialog):
    def __init__(self,gui_worker,desid):
        super().__init__()
        self.setWindowTitle('添加好友请求')
        self.resize(160, 150)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.interface = gui_worker
        self.id2confirm = desid

        ###### 设置界面控件
        self.frame = QtWidgets.QFrame(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)

        self.account = QtWidgets.QLabel()
        self.account.setText("对方学号："+self.id2confirm)
        self.verticalLayout.addWidget(self.account)
 
        self.pushButton_enter = QtWidgets.QPushButton()
        self.pushButton_enter.setText("接受")
        self.verticalLayout.addWidget(self.pushButton_enter)
 
        self.pushButton_quit = QtWidgets.QPushButton()
        self.pushButton_quit.setText("拒绝")
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(self.close)

    def on_pushButton_enter_clicked(self):
        self.interface.confirmfriend(self.id2confirm)  
        self.accept()

    def close(self):
        # self.interface.rejectfriend(self.id2confirm)
        self.reject()

class confirmvideodialog(QtWidgets.QDialog):
    def __init__(self,gui_worker,desid):
        super().__init__()
        self.setWindowTitle('请求视频')
        self.resize(160, 150)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.interface = gui_worker
        self.id2confirm = desid

        ###### 设置界面控件
        self.frame = QtWidgets.QFrame(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)

        self.account = QtWidgets.QLabel()
        self.account.setText("对方学号："+self.id2confirm)
        self.verticalLayout.addWidget(self.account)
 
        self.pushButton_enter = QtWidgets.QPushButton()
        self.pushButton_enter.setText("接受")
        self.verticalLayout.addWidget(self.pushButton_enter)
 
        self.pushButton_quit = QtWidgets.QPushButton()
        self.pushButton_quit.setText("拒绝")
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(self.close)

    def on_pushButton_enter_clicked(self):
        # self.interface.confirmvideo(self.id2confirm)  
        self.accept()

    def close(self):
        # self.interface.rejectfriend(self.id2confirm)
        self.reject()



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.ui_mainwindow import Ui_MainWindow
from Chatter.data_type import *

class MainWindow(QtWidgets.QMainWindow):
    windowsList = []
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
        self.functional_group.addButton(self.ui.pushButton_5,3)

        #slot
        self.ui.addfriend.clicked.connect(self.addfriend)
        self.functional_group.buttonClicked.connect(self.functionalchange)


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
            if ip=='n':
                new.setForeground(QtGui.QBrush(QtCore.Qt.red))
            else:
                new.setForeground(QtGui.QBrush(QtCore.Qt.green))
            self.ui.contacts.addItem(new)
    
    def functionalchange(self,button):
        self.current_datatype = data[button.text()].value
    
    def send_msg(self):
        pass#TODO: 


    

class logindialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('登录界面')
        self.resize(160, 150)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
 
        ###### 设置界面控件
        self.frame = QtWidgets.QFrame(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
 
        self.lineEdit_account = QtWidgets.QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        self.verticalLayout.addWidget(self.lineEdit_account)
 
        self.lineEdit_password = QtWidgets.QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        self.verticalLayout.addWidget(self.lineEdit_password)
 
        self.pushButton_enter = QtWidgets.QPushButton()
        self.pushButton_enter.setText("确定")
        self.verticalLayout.addWidget(self.pushButton_enter)
 
        self.pushButton_quit = QtWidgets.QPushButton()
        self.pushButton_quit.setText("取消")
        self.verticalLayout.addWidget(self.pushButton_quit)
 
        ###### 绑定按钮事件
        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QtCore.QCoreApplication.instance().quit)
 
 
 
 
    def on_pushButton_enter_clicked(self):
        #TODO: normalized judgment
        if self.lineEdit_account.text() == "":
            return
 
        # 密码判断
        if self.lineEdit_password.text() == "":
            return
 
        # 通过验证，关闭对话框并返回1
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
        tmp = self.interface.addfriends(self.lineEdit_account.text())
        if tmp == None:
            QtWidgets.QMessageBox().warning(self,"提醒","No Such Person!")
        else:
            QtWidgets.QMessageBox().information(self,"提示","Successfully Added!")
        
        self.accept()



# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(908, 539)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.message = QtWidgets.QListWidget(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(300, 0, 611, 451))
        self.message.setObjectName("message")
        self.editor = QtWidgets.QTextEdit(self.centralwidget)
        self.editor.setGeometry(QtCore.QRect(300, 480, 541, 61))
        self.editor.setObjectName("editor")
        self.sendmsg = QtWidgets.QPushButton(self.centralwidget)
        self.sendmsg.setGeometry(QtCore.QRect(840, 480, 71, 61))
        self.sendmsg.setObjectName("sendmsg")
        self.text_send = QtWidgets.QPushButton(self.centralwidget)
        self.text_send.setGeometry(QtCore.QRect(300, 450, 81, 31))
        self.text_send.setCheckable(True)
        self.text_send.setChecked(True)
        self.text_send.setObjectName("text_send")
        self.file_send = QtWidgets.QPushButton(self.centralwidget)
        self.file_send.setGeometry(QtCore.QRect(380, 450, 81, 31))
        self.file_send.setCheckable(True)
        self.file_send.setObjectName("file_send")
        self.video_send = QtWidgets.QPushButton(self.centralwidget)
        self.video_send.setGeometry(QtCore.QRect(460, 450, 81, 31))
        self.video_send.setCheckable(True)
        self.video_send.setObjectName("video_send")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(60, 0, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.contacts = QtWidgets.QListWidget(self.centralwidget)
        self.contacts.setGeometry(QtCore.QRect(0, 60, 301, 481))
        self.contacts.setObjectName("contacts")
        self.removefriend = QtWidgets.QPushButton(self.centralwidget)
        self.removefriend.setGeometry(QtCore.QRect(0, 0, 61, 61))
        self.removefriend.setCheckable(True)
        self.removefriend.setObjectName("removefriend")
        self.addfriend = QtWidgets.QPushButton(self.centralwidget)
        self.addfriend.setGeometry(QtCore.QRect(240, 0, 61, 61))
        self.addfriend.setObjectName("addfriend")
        self.quitvideo = QtWidgets.QPushButton(self.centralwidget)
        self.quitvideo.setEnabled(False)
        self.quitvideo.setGeometry(QtCore.QRect(820, 450, 89, 31))
        self.quitvideo.setObjectName("quitvideo")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sendmsg.setText(_translate("MainWindow", "发送"))
        self.text_send.setText(_translate("MainWindow", "text"))
        self.file_send.setText(_translate("MainWindow", "file"))
        self.video_send.setText(_translate("MainWindow", "video"))
        self.title.setText(_translate("MainWindow", "Contacts"))
        self.removefriend.setText(_translate("MainWindow", "工具"))
        self.addfriend.setText(_translate("MainWindow", "添加"))
        self.quitvideo.setText(_translate("MainWindow", "退出视频"))

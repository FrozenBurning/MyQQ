import socket
import threading
import os
import json
import time
from Chatter.data_type import data

class ChatSender(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = None
        self.port = None
        self.srcid = None
        self.desid = None

    def run(self):
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect((self.address, self.port))
        # print(data['text'].value)
        # test str sending
        # while True:
        #     message = input("Your message > ")
        #     try:
        #         send_socket.send(message.encode())
        #     except:
        #         Exception
        #     if message.lower() == "quit":
        #         break
        file_path = '/home/royubuntu/ComputerNetwork/MyQQ/alabama.jpg'
        #test file sending
        while True:
            command = input("Send text or image (T) or (I) >")
            if command.lower() == 't':
                message = input("Your message > ")
                send_socket.send(json.dumps(self.header_data_wrapper(data['text'].value)).encode())  
                reply = send_socket.recv(1)

                if ord(reply) == 1:
                    print('header has been recved!')          

                send_socket.sendall(message.encode())    
            elif command.lower() == 'i':
                send_socket.send(json.dumps(self.header_data_wrapper(data['file'].value,file_path)).encode())
                reply = send_socket.recv(1)
                # while reply!=1:
                #     send_socket.send(json.dumps(header_data_wrapper()))
                #     reply = send_socket.recv(1)
                # header recved
                if ord(reply) == 1:
                    print('header has been recved!')

                f = open(file_path,'rb')
                content = f.read()
                send_socket.sendall(content)
    
    def header_data_wrapper(self,data_type,file_path=None):
        more = {}
        if data_type == data['file'].value and file_path != None:
            file_name = file_path.rsplit(os.sep,1)[1]
            file_size = os.path.getsize(file_path)
            more = {
                'file_name':file_name,
                'file_size':file_size,
                'charset':'utf-8'
            }

        header_data = {
            'sender_id':self.srcid,
            'recver_id':self.desid,
            'data_type':data_type,
            'date':time.strftime('%Y-%m-%d %X',time.localtime()),
            'optional':more            
        }
        return header_data
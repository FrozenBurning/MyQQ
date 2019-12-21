import socket
import threading
import os
import json
import time
from Chatter.data_type import *

class ChatSender(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = None
        self.port = None
        self.srcid = None
        self.desid = None
        self.worker_type = worker_type['sender'].value
        self.buffer = []

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
        #test file sending
        # while True:
        #     command = input("Send text or image (T) or (I) >")
        #     if command.lower() == 't':
        #         message = input("Your message > ")
        #         send_socket.send(json.dumps(self.header_data_wrapper(data['text'].value)).encode())  
        #         reply = send_socket.recv(1)

        #         if ord(reply) == 1:
        #             print('header has been recved!')          

        #         send_socket.sendall(message.encode())    
        #     elif command.lower() == 'i':
        #         send_socket.send(json.dumps(self.header_data_wrapper(data['file'].value,file_path)).encode())
        #         reply = send_socket.recv(1)
        #         # while reply!=1:
        #         #     send_socket.send(json.dumps(header_data_wrapper()))
        #         #     reply = send_socket.recv(1)
        #         # header recved
        #         if ord(reply) == 1:
        #             print('header has been recved!')

        #         f = open(file_path,'rb')
        #         content = f.read()
        #         send_socket.sendall(content)

        while True:
            if len(self.buffer) == 0:
                time.sleep(0.05)
                continue
            
            current_msg = self.buffer.pop()

            if current_msg['data_type'] == data['command'].value:
                if current_msg['optional']['command_type']== command_type['disconnect'].value or \
                    current_msg['optional']['command_type']== command_type['logout'].value:
                    send_socket.close()
                    return
                elif current_msg['optional']['command_type']==command_type['hi'].value:
                    send_socket.send(json.dumps(self.header_data_wrapper(current_msg['data_type'],current_msg['data'])).encode())  
                    reply = send_socket.recv(1)

                    if ord(reply) == 1:
                        print('header has been recved!')  
                    send_socket.sendall(current_msg['data'].encode())
                elif current_msg['optional']['command_type']==command_type['reject'].value:
                    send_socket.send(json.dumps(self.header_data_wrapper(current_msg['data_type'],current_msg['data'])).encode())  
                    reply = send_socket.recv(1)

                    if ord(reply) == 1:
                        print('header has been recved!') 
                    send_socket.sendall(current_msg['data'].encode())
                    send_socket.close()
                    return


            else:#messaging
                send_socket.send(json.dumps(self.header_data_wrapper(current_msg['data_type'],current_msg['data'])).encode())  
                reply = send_socket.recv(1)

                if ord(reply) == 1:
                    print('header has been recved!')     #TODO:

                if current_msg['data_type'] == data['file'].value:
                    f = open(current_msg['data'],'rb')
                    content = f.read()
                    send_socket.sendall(content)
                    f.close()
                elif current_msg['data_type'] == data['text'].value:
                    send_socket.sendall(current_msg['data'].encode())
                    

                    

                
    
    def send(self, msg):
        self.buffer.append(msg)

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
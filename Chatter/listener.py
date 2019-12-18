import socket
import threading
import os
import json
import time
from Chatter.data_type import *


LOCALHOST = '0.0.0.0'
BUFFER_SIZE = 1024

class ChatListener(threading.Thread):

        def __init__(self,router):
            threading.Thread.__init__(self)
            self.port = None
            self.worker_type = worker_type['listener'].value
            self.router = router

        def run(self):
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.bind((LOCALHOST, self.port))
            listen_socket.listen(10)
            while True:
                connection, address = listen_socket.accept()
                p = threading.Thread(target=self.recv_data,args=(connection,address,self.router))
                p.start()


        def recv_data(self, new_socket,client_info,router):
            print("Established connection with: ", client_info)
            while True:
                total_data = b''
                header = new_socket.recv(BUFFER_SIZE)
                if len(header) == 0:
                    continue

                recv_header = json.loads(header)
                print(recv_header)
                if recv_header['data_type']==data['text'].value:
                    #ack
                    new_socket.send(bytes([1]))
                    message = new_socket.recv(BUFFER_SIZE).decode()
                    print("Recv: ", message,"from (",client_info,")")
                    router.recv(message,self.worker_type,worker_type['gui'].value,data['text'].value)       
                elif recv_header['data_type'] == data['file'].value:
                    res_name = recv_header['optional']['file_name']
                    res_size = recv_header['optional']['file_size']
                    #ack
                    new_socket.send(bytes([1]))
                    num = res_size/1024.0
                    if num != int(num):
                        num = int(num) +1
                    else:
                        num = int(num)
                    for i in range(num):
                        content = new_socket.recv(BUFFER_SIZE)
                        total_data += content
                    with open("recved_"+recv_header['optional']['file_name'],"wb") as f:
                        f.write(total_data)

                    router.recv(total_data,self.worker_type,worker_type['gui'].value,data['file'].value)                           
            new_socket.close() #TODO: 
            
                



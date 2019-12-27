import socket
import threading
import os
import json
import time
from Chatter.data_type import *

# 绑定本地9876端口
LOCALHOST = '0.0.0.0'
LOCALPORT = 9876
BUFFER_SIZE = 1024

# Listener
class ChatListener(threading.Thread):

        def __init__(self,router):
            threading.Thread.__init__(self)
            self.port =LOCALPORT
            self.worker_type = worker_type['listener'].value
            # 线程“路由”句柄
            self.router = router
            self.daemon=True

        def run(self):
            # 监听连接请求
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.bind((LOCALHOST, self.port))
            listen_socket.listen(10)
            while True:
                # 创建服务socket 开辟子线程用于服务，并返回监听状态
                connection, address = listen_socket.accept()
                p = threading.Thread(target=self.recv_data,daemon=True,args=(connection,address,self.router))
                p.start()

        # 服务线程主体
        def recv_data(self, new_socket,client_info,router):
            print("Established connection with: ", client_info)
            while True:
                total_data = b''
                header = new_socket.recv(BUFFER_SIZE)
                if len(header) == 0:
                    continue
                
                # 解封装数据报报头
                recv_header = json.loads(header)
                print(recv_header)

                # 根据数据类型进行接收，并通过线程路由recv将数据推送给线程“路由”
                if recv_header['data_type']==data['text'].value:
                    #ack
                    new_socket.send(bytes([1]))
                    message = new_socket.recv(BUFFER_SIZE).decode()
                    print("Recv: ", message,"from (",client_info,")")
                    router.recv(message,recv_header['sender_id'],worker_type['gui'].value,data['text'].value)       
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
                    filepath = "recved_"+recv_header['optional']['file_name']
                    with open(filepath,"wb") as f:
                        f.write(total_data)

                    router.recv(filepath,recv_header['sender_id'],worker_type['gui'].value,data['file'].value)                           
                elif recv_header['data_type'] == data['command'].value:
                    #ack
                    new_socket.send(bytes([1]))
                    command = new_socket.recv(BUFFER_SIZE).decode()
                    print("Recv Command",command)
                    router.recv(command,recv_header['sender_id'],worker_type['gui'].value,data['command'].value)
            
            new_socket.close()
            
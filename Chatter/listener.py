import socket
import threading
import os
import json
import time

LOCALHOST = '0.0.0.0'
BUFFER_SIZE = 1024

class ChatListener(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.port = None

        def run(self):
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.bind((LOCALHOST, self.port))
            listen_socket.listen(1)
            connection, address = listen_socket.accept()
            print("Established connection with: ", address)

            # test str
            # while True:
            #     message = connection.recv(BUFFER_SIZE).decode()
            #     print("Recv: ", message,"(from %s)",address)
            #     if message.lower() == "quit":
            #         break

            # test file 
            while True:
                total_data = b''
                header = connection.recv(BUFFER_SIZE)
                if len(header) == 0:
                    continue

                recv_header = json.loads(header)
                print(recv_header)
                res_name = recv_header['file_name']
                res_size = recv_header['file_size']
                
                #ack
                connection.send(bytes([1]))
                num = res_size/1024.0
                if num != int(num):
                    num = int(num) +1
                else:
                    num = int(num)

                for i in range(num):
                    content = connection.recv(BUFFER_SIZE)
                    total_data += content
                
                with open("11.png","wb") as f:
                    f.write(total_data)
                    
                



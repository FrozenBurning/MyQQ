import socket
import threading
import os
import json
import time

def header_data_wrapper(file_path):
    file_name = file_path.rsplit(os.sep,1)[1]
    file_size = os.path.getsize(file_path)
    header_data = {
        'file_name':file_name,
        'file_size':file_size,
        'data':time.strftime('%Y-%m-%d %X',time.localtime()),
        'charset':'utf-8'
    }
    return header_data

class ChatSender(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.address = None
            self.port = None

        def run(self):
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.connect((self.address, self.port))

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
                command = input("Ready to send image? >")
                send_socket.send(json.dumps(header_data_wrapper(file_path)).encode())
                reply = send_socket.recv(1)
                # while reply!=1:
                #     send_socket.send(json.dumps(header_data_wrapper()))
                #     reply = send_socket.recv(1)
                # header recved
                if ord(reply) == 1:
                    print('header recved!')
                
                f = open(file_path,'rb')
                content = f.read()

                send_socket.sendall(content)





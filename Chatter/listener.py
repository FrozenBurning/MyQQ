import socket
import threading

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
            while True:
                message = connection.recv(BUFFER_SIZE).decode()
                print("Recv: ", message,"(from %s)",address)
                if message.lower() == "quit":
                    break

import socket
import threading

class ChatSender(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.address = None
            self.port = None

        def run(self):
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.connect((self.address, self.port))

            while True:
                message = input("Your message > ")
                try:
                    send_socket.send(message.encode())
                except:
                    Exception
                if message.lower() == "quit":
                    break

import cv2
import socket
from imutils.video import WebcamVideoStream
import pyaudio
from array import array
from threading import Thread
import numpy as np
import zlib
import struct

# REMOTEHOST = input("Enter Server IP\n")
PORT4VIDEO = 3000
PORT4AUDIO = 4000

BufferSize = 4096
CHUNK=1024
lnF = 640*480*3
FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100

class MediaClient():
    def __init__(self,remotehost):
        super().__init__()
        try:
            self.clientVideoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientVideoSocket.connect((remotehost, PORT4VIDEO))
        except OSError:
            print("Server video port Refuse")
            return
        self.videostream = WebcamVideoStream(0).start()

        try:
            self.clientAudioSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientAudioSocket.connect((remotehost, PORT4AUDIO))
        except OSError:
            print("Server audio port refuse")
            return 
        
        self.audio=pyaudio.PyAudio()
        self.audiostream=self.audio.open(format=FORMAT,channels=CHANNELS, rate=RATE, input=True, output = True,frames_per_buffer=CHUNK)
        self.working = True
        #wait for connection
        initiation = self.clientVideoSocket.recv(5).decode()

        if initiation == "start":
            SendFrameThread = Thread(target=self.SendFrame).start()
            SendAudioThread = Thread(target=self.SendAudio).start()
            RecieveFrameThread = Thread(target=self.RecieveFrame).start()
            RecieveAudioThread = Thread(target=self.RecieveAudio).start()


    def SendAudio(self):
        while self.working:
            data = self.audiostream.read(CHUNK)
            dataChunk = array('h', data)
            vol = max(dataChunk)
            if(vol > 500):
                print("Recording Sound...")
            else:
                print("Silence..")
            self.clientAudioSocket.sendall(data)

    def RecieveAudio(self):
        while self.working:
            data = self.recvallAudio(BufferSize)
            self.audiostream.write(data)

    def recvallAudio(self,size):
        databytes = b''
        while len(databytes) != size:
            to_read = size - len(databytes)
            if to_read > (4 * CHUNK):
                databytes += self.clientAudioSocket.recv(4 * CHUNK)
            else:
                databytes += self.clientAudioSocket.recv(to_read)
        return databytes

    def SendFrame(self):
        while self.working:
            try:
                frame = self.videostream.read()
                cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                frame = np.array(frame, dtype = np.uint8).reshape(1, lnF)
                jpg_as_text = bytearray(frame)

                databytes = zlib.compress(jpg_as_text, 9)
                length = struct.pack('!I', len(databytes))
                bytesToBeSend = b''
                self.clientVideoSocket.sendall(length)
                while len(databytes) > 0:
                    if (5000 * CHUNK) <= len(databytes):
                        bytesToBeSend = databytes[:(5000 * CHUNK)]
                        databytes = databytes[(5000 * CHUNK):]
                        self.clientVideoSocket.sendall(bytesToBeSend)
                    else:
                        bytesToBeSend = databytes
                        self.clientVideoSocket.sendall(bytesToBeSend)
                        databytes = b''
                print("##### Data Sent!! #####")
            except:
                continue


    def RecieveFrame(self):
        while self.working:
            try:
                lengthbuf = self.recvallVideo(4)
                length, = struct.unpack('!I', lengthbuf)
                databytes = self.recvallVideo(length)
                img = zlib.decompress(databytes)
                if len(databytes) == length:
                    print("Recieving Media..")
                    print("Image Frame Size:- {}".format(len(img)))
                    img = np.array(list(img))
                    img = np.array(img, dtype = np.uint8).reshape(480, 640, 3)
                    cv2.imshow("Received Video", img)
                    if cv2.waitKey(1) == 27:
                        cv2.destroyAllWindows()
                else:
                    print("Data CORRUPTED")
            except:
                continue


    def recvallVideo(self,size):
        databytes = b''
        while len(databytes) != size:
            to_read = size - len(databytes)
            if to_read > (5000 * CHUNK):
                databytes += self.clientVideoSocket.recv(5000 * CHUNK)
            else:
                databytes += self.clientVideoSocket.recv(to_read)
        return databytes


c = MediaClient("127.0.0.1")
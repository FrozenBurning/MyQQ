import cv2
import socket
from imutils.video import WebcamVideoStream
import pyaudio
from array import array
from threading import Thread
import numpy as np
import zlib
import struct

# HOST = input("Enter Host IP\n")
PORT4VIDEO = 3000
PORT4AUDIO = 4000


BufferSize = 4096
CHUNK=1024
lnF = 640*480*3
FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100


class MediaServer():
    def __init__(self):
        super().__init__()
        self.serverAudio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serverAudio.bind(("0.0.0.0", PORT4AUDIO))
        except OSError:
            print("Server Busy")

        self.serverVideo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serverVideo.bind(("0.0.0.0", PORT4VIDEO))
        except OSError:
            print("Server Busy")

        self.serverAudio.listen(1)
        self.serverVideo.listen(1)

        self.clientAudio,self.addraudio = self.serverAudio.accept()
        self.clientVideo,self.addrvideo = self.serverVideo.accept()
        
        self.videostream = WebcamVideoStream(0).start()
        self.audio=pyaudio.PyAudio()
        self.audiostream=self.audio.open(format=FORMAT,channels=CHANNELS, rate=RATE, input=True, output = True,frames_per_buffer=CHUNK)


        self.clientVideo.send("start".encode())
        # SendFrameThread = Thread(target=self.SendFrame).start()
        # SendAudioThread = Thread(target=self.SendAudio).start()
        RecieveFrameThread = Thread(target=self.RecieveFrame).start()
        RecieveAudioThread = Thread(target=self.RecieveAudio).start()

    def SendAudio(self):
        while True:
            data = self.audiostream.read(CHUNK)
            dataChunk = array('h', data)
            vol = max(dataChunk)
            if(vol > 500):
                print("Recording Sound...")
            else:
                print("Silence..")
            self.clientAudio.sendall(data)

    def RecieveAudio(self):
        while True:
            data = self.recvallAudio(BufferSize)
            self.audiostream.write(data)

    def recvallAudio(self,size):
        databytes = b''
        while len(databytes) != size:
            to_read = size - len(databytes)
            if to_read > (4 * CHUNK):
                databytes += self.clientAudio.recv(4 * CHUNK)
            else:
                databytes += self.clientAudio.recv(to_read)
        return databytes

    def SendFrame(self):
        while True:
            try:
                frame = self.videostream.read()
                cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                frame = np.array(frame, dtype = np.uint8).reshape(1, lnF)
                jpg_as_text = bytearray(frame)

                databytes = zlib.compress(jpg_as_text, 9)
                length = struct.pack('!I', len(databytes))
                bytesToBeSend = b''
                self.clientVideo.sendall(length)
                while len(databytes) > 0:
                    if (5000 * CHUNK) <= len(databytes):
                        bytesToBeSend = databytes[:(5000 * CHUNK)]
                        databytes = databytes[(5000 * CHUNK):]
                        self.clientVideo.sendall(bytesToBeSend)
                    else:
                        bytesToBeSend = databytes
                        self.clientVideo.sendall(bytesToBeSend)
                        databytes = b''
                print("##### Data Sent!! #####")
            except:
                continue


    def RecieveFrame(self):
        while True:
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
                databytes += self.clientVideo.recv(5000 * CHUNK)
            else:
                databytes += self.clientVideo.recv(to_read)
        return databytes


m = MediaServer()

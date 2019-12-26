import cv2
import socket
from imutils.video import WebcamVideoStream
import pyaudio
from array import array
from threading import Thread
import numpy as np
import zlib
import struct
import time
import matplotlib.pyplot as plt
import queue
# HOST = input("Enter Host IP\n")
PORT4VIDEO = 3000
PORT4AUDIO = 4000


BufferSize = 4096
CHUNK=1024
lnF = 640*480*3
FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100

class MediaServer(Thread):
    def __init__(self):
        Thread.__init__(self,daemon=True)
        self.working = False
        self.video = queue.Queue()
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
        self.RecieveFrameThread = Thread(name='recframe',target=self.RecieveFrame,daemon=True)
        self.RecieveAudioThread = Thread(name='recaudio',target=self.RecieveAudio,daemon=True)

    
    def run(self):
        self.RecieveFrameThread.start()
        self.RecieveAudioThread.start()
        while True:
            try:
                self.serverAudio.listen(1)
                self.serverVideo.listen(1)
                print("waiting connection...")
                try:
                    plt.close()
                except:
                    pass
                self.clientAudio,self.addraudio = self.serverAudio.accept()
                self.clientVideo,self.addrvideo = self.serverVideo.accept()
                print("accept connection @",self.addrvideo)
                self.working=True
                # self.videostream = WebcamVideoStream(0).start()
                self.audio=pyaudio.PyAudio()
                try:
                    self.audiostream=self.audio.open(format=FORMAT,channels=CHANNELS, rate=RATE,output = True,frames_per_buffer=CHUNK)
                except:
                    print("fucking damn audio card!")
                # cv2.startWindowThread()
                # cv2.namedWindow("Receive Video")
                self.clientVideo.send("start".encode())
                # SendFrameThread = Thread(target=self.SendFrame).start()
                # SendAudioThread = Thread(target=self.SendAudio).start()

                # self.RecieveFrameThread.join()
                # self.RecieveAudioThread.join()
                while self.working:
                    time.sleep(1)
                #     print(self.video.qsize())
                #     img = self.video.get(block=True)
                #     cv2.imshow("Receive Video",img)
                # print("working",self.working)
                # time.sleep(5)

                self.clientAudio.close()
                self.clientVideo.close()
                self.audiostream.close()
            except:
                time.sleep(5)


    def RecieveAudio(self):
        while True:
            if self.working:
                data = self.recvallAudio(BufferSize)
                try:
                    self.audiostream.write(data)
                except OSError:
                    print("receive audio thread end")
                    continue
            else:
                time.sleep(1)
    def recvallAudio(self,size):
        databytes = b''
        while len(databytes) != size and self.working:
            to_read = size - len(databytes)
            if to_read > (4 * CHUNK):
                databytes += self.clientAudio.recv(4 * CHUNK)
            else:
                databytes += self.clientAudio.recv(to_read)
        return databytes



    def RecieveFrame(self):
        plt.figure(1)
        # handler = plt.imshow(np.zeros((480,640,3)))
        plt.axis('off')
        while True:
            if self.working:
                try:
                    lengthbuf = self.recvallVideo(4)
                    length, = struct.unpack('!I', lengthbuf)
                    databytes = self.recvallVideo(length)
                    img = zlib.decompress(databytes)
                    if len(databytes) == length:
                        # print("Recieving Media..")
                        # print("Image Frame Size:- {}".format(len(img)))
                        img = np.array(list(img))
                        img = np.array(img, dtype = np.uint8).reshape(480, 640, 3)
                        plt.imshow(img)
                        plt.pause(0.03)
                        # newimg = np.zeros((240,480))
                        # self.video.put(img)
                        # cv2.imshow("Received Video", img)
                        # cv2.waitKey(30)
                    else:
                        print("Data CORRUPTED")
                except:
                    continue
                    # if len(lengthbuf)==0:
                    #     break
                    # else:
                    #     continue
            else:
                time.sleep(1)
                # print("receive frame thread end")
                cv2.destroyAllWindows()
                # cv2.waitKey(100)
        return


    def recvallVideo(self,size):
        databytes = b''
        timer = 0
        while len(databytes) != size and self.working:
            # print(timer)
            if timer >  50000:
                # self.videostream.stop()
                self.audiostream.close()
                self.working = False
                #fresh buffer
                databytes += self.clientVideo.recv(5000 * CHUNK)
                return b''
            to_read = size - len(databytes)
            if to_read > (5000 * CHUNK):
                databytes += self.clientVideo.recv(5000 * CHUNK)
            else:
                databytes += self.clientVideo.recv(to_read)
            
            timer+=1
        return databytes
        


# m = MediaServer()
# m.start()
# # cv2.namedWindow("Receive Video")

# while True:

#     print("get img!")
#     try:
#         img = m.video.get(block=True,timeout=3)
#     except:
#         cv2.destroyAllWindows()
#         continue
#     print("size:",np.size(img))
#     cv2.imshow("Receive Video",img)
#     if cv2.waitKey(30)==27:
#         # self.videostream.stop()
#         print("ESC Pressed!")
#         m.working = False        
#         time.sleep(2)

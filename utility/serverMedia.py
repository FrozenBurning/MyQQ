import cv2
import socket
import pyaudio
from array import array
from threading import Thread
import numpy as np
import zlib
import struct
import time
import matplotlib.pyplot as plt
import queue

# 音视频监听端口
PORT4VIDEO = 3333
PORT4AUDIO = 4444

# 音视频动态参数
BufferSize = 4096
CHUNK=1024
lnF = 640*480*3
FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100

class MediaServer(Thread):
    def __init__(self):
        Thread.__init__(self,daemon=True)
        #工作标志
        self.working = False
        #deprecated
        self.video = queue.Queue()
        #音频socket
        self.serverAudio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serverAudio.bind(("0.0.0.0", PORT4AUDIO))
        except OSError:
            print("Server Busy")

        #视频socket
        self.serverVideo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serverVideo.bind(("0.0.0.0", PORT4VIDEO))
        except OSError:
            print("Server Busy")     
        # 创建接受音视频流线程，但不开始   
        self.ReceivingFrameThread = Thread(name='recframe',target=self.RecieveFrame,daemon=True)
        self.ReceivingAudioThread = Thread(name='recaudio',target=self.RecieveAudio,daemon=True)

    
    def run(self):
        #一直运行
        self.ReceivingFrameThread.start()
        self.ReceivingAudioThread.start()
        while True:
            try:
                # 监听连接请求
                self.serverAudio.listen(1)
                self.serverVideo.listen(1)
                print("waiting connection...")
                try:
                    plt.close()
                except:
                    pass
                # 新建socket服务对应连接
                self.clientAudio,self.addraudio = self.serverAudio.accept()
                self.clientVideo,self.addrvideo = self.serverVideo.accept()
                print("accept connection @",self.addrvideo)
                # 开始工作
                self.working=True

                # 硬件准备
                self.audio=pyaudio.PyAudio()
                try:
                    self.audiostream=self.audio.open(format=FORMAT,channels=CHANNELS, rate=RATE,output = True,frames_per_buffer=CHUNK)
                except:
                    print("audio card cant output!")

                #发送开始标志
                self.clientVideo.send("start".encode())

                # 监听线程进入等待 直到当前的音视频服务结束
                while self.working:
                    time.sleep(1)

                #回收服务socket 重启设备
                self.clientAudio.close()
                self.clientVideo.close()
                self.audiostream.close()

                # 监听线程重新回到监听状态 等待下一次音视频流连接请求
            except:
                time.sleep(5)

    # 接受音频
    def RecieveAudio(self):
        while True:
            if self.working:
                data = self.recvallAudio(BufferSize)
                try:
                    self.audiostream.write(data)
                except OSError:
                    print("receive audio thread reset")
                    continue
            else:
                time.sleep(1)
    
    # 音频分块接受
    def recvallAudio(self,size):
        databytes = b''
        while len(databytes) != size and self.working:
            to_read = size - len(databytes)
            if to_read > (4 * CHUNK):
                databytes += self.clientAudio.recv(4 * CHUNK)
            else:
                databytes += self.clientAudio.recv(to_read)
        return databytes


    # 接受视频
    def RecieveFrame(self):
        plt.figure(1)
        # handler = plt.imshow(np.zeros((480,640,3)))
        plt.axis('off')
        while True:
            if self.working:
                try:
                    # 接受当前帧长度
                    lengthbuf = self.recvallVideo(4)
                    length, = struct.unpack('!I', lengthbuf)
                    # 根据长度开辟内存接受帧
                    databytes = self.recvallVideo(length)
                    # 解压缩
                    img = zlib.decompress(databytes)
                    if len(databytes) == length:
                        # 去序列化
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
                # cv2.destroyAllWindows()
                # cv2.waitKey(100)
        return

    # 分块接收单一视频帧
    def recvallVideo(self,size):
        databytes = b''
        timer = 0
        while len(databytes) != size and self.working:
            # print(timer)
            # 连接超时判据 重置servermedia服务
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
        

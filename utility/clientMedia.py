import cv2
import socket
import pyaudio
from array import array
from threading import Thread
import numpy as np
import zlib
import struct
import time

# 音视频监听端口
PORT4VIDEO = 3333
PORT4AUDIO = 4444

# 解码、数据流参数
BufferSize = 4096
CHUNK=1024
lnF = 640*480*3
FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100

class MediaClient(Thread):
    def __init__(self):
        Thread.__init__(self,daemon=True)
        # 工作标志
        self.working=False
        # 连接的远端ip
        self.remote = None

    # 线程主体
    def run(self):
        try:
            # 视频socket
            self.clientVideoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientVideoSocket.connect((self.remote, PORT4VIDEO))
        except OSError:
            print("Server video port Refuse")
            return
        # 视频流
        self.videostream = cv2.VideoCapture(0)

        try:
            # 音频socket
            self.clientAudioSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientAudioSocket.connect((self.remote, PORT4AUDIO))
        except OSError:
            print("Server audio port refuse")
            return 
        # 等待硬件启动
        time.sleep(1)
        # 音频流
        self.audio=pyaudio.PyAudio()
        try:
            self.audiostream=self.audio.open(format=FORMAT,channels=CHANNELS, rate=RATE, input=True,frames_per_buffer=CHUNK)
            self.working = True
        except:
            print("no audio")
        # 硬件正常启动 Socket工作正常
        if self.working:
            #wait for connection
            initiation = self.clientVideoSocket.recv(5).decode()
            if initiation == "start":
                SendFrameThread = Thread(name='sendframe',daemon=True,target=self.SendFrame)
                SendAudioThread = Thread(name='sendaudio',daemon=True,target=self.SendAudio)
                SendFrameThread.start()
                SendAudioThread.start()
                # 两个流阻塞当前线程
                SendFrameThread.join()
                SendAudioThread.join()
        

    # 音频流发送
    def SendAudio(self):
        while self.working:
            # 读取音频
            data = self.audiostream.read(CHUNK)
            dataChunk = array('h', data)
            vol = max(dataChunk)
            # 阈值去噪
            if(vol > 500):
                print("Recording Sound...")
            else:
                pass
                # print("Silence..")
            try:
                self.clientAudioSocket.sendall(data)
            except:
                print("radio socket shut down")
                break
        # 线程结束 回收内存和相应句柄
        self.clientAudioSocket.close()
        self.audiostream.close()

    # 视频流发送
    def SendFrame(self):
        while self.working:
            try:
                # 读取视频帧
                (grab,frame) = self.videostream.read()
                # opencv使用BGR色彩空间 需要转换为RGB进行显示
                cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2_im
                frame = cv2.resize(frame, (640, 480))
                frame = np.array(frame, dtype = np.uint8).reshape(1, lnF)
                # 序列化
                jpg_as_text = bytearray(frame)
                # 压缩
                databytes = zlib.compress(jpg_as_text, 9)
                # 单帧图片压缩后长度
                length = struct.pack('!I', len(databytes))
                bytesToBeSend = b''
                try:
                    # 发送当前帧长度通知对方准备相应资源接受
                    self.clientVideoSocket.sendall(length)
                except:
                    print("cant send video!")
                    self.working=False
                    break
                # 发送当前帧数据
                while len(databytes) > 0:
                    # 分块发送
                    if (5000 * CHUNK) <= len(databytes):
                        bytesToBeSend = databytes[:(5000 * CHUNK)]
                        databytes = databytes[(5000 * CHUNK):]
                        try:
                            self.clientVideoSocket.sendall(bytesToBeSend)
                        except:
                            print("cant send video!")
                            self.working=False
                            break
                    else:
                        bytesToBeSend = databytes
                        try:
                            self.clientVideoSocket.sendall(bytesToBeSend)
                        except:
                            print("cant send video!")
                            self.working=False
                            break
                        databytes = b''
            except:
                continue
        # 线程结束回收资源和句柄
        self.clientVideoSocket.close()
        self.videostream.release()
        
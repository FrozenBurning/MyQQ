import threading

class thread_1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.numlist = []
    def run(self):
        while True:
            if len(self.numlist):
                print(self.numlist)
            # print(threading.current_thread().name)
    def add(self):
        self.numlist.append(1)

class thread_2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.numlist = []
    def run(self):
        while True:
            if len(self.numlist):
                print(self.numlist)
            # print(threading.current_thread().name)
    def add(self):
        self.numlist.append(2)
        
# def thread_1():
#  # current_thread().name | 线程名称
#     while True:
#         print(threading.current_thread().name)

# def thread_2():
#     while True:
#         print(threading.current_thread().name)

# 定义任务
# t1 = threading.Thread(target=thread_1, args=(), name='Thread_1') # name 定义线程名称
# t2 = threading.Thread(target=thread_2, args=(), name='Thread_2') 
t1 = thread_1()
t2 = thread_2()
# 启动任务
print(threading.current_thread().name) # 当前进程名称
t1.start() # 同步 t1.join | 结束 t1.terminate()
t2.start()
while True:
    command = input("append num? >")
    if command=='1':
        t1.add()
    else:
        t2.add()
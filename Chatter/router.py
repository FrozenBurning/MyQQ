from Chatter.data_type import *
from Chatter.listener import *
from Chatter.sender import *
from utility.connectiontool import *
import queue
from contextlib import contextmanager

#线程“路由”
class router(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # 消息池
        self.messagepool = queue.Queue()
        # 订阅者集合，即所有的consumer
        self._subscribers = set()
        self.sok2server = ConnectionTool()
        self.working = True
        self.myid = None

    def run(self):
        # 一直执行路由
        self.sok2server.ConnectionInit()
        while self.working:
            self.routing()

    # 接入一个consumer
    def attach(self, task):
        self._subscribers.add(task)

    #注销一个consumer
    def detach(self, task):
        self._subscribers.remove(task)

    # 供外部producter调用
    def recv(self,data, sender_type,recver_type,data_type,destination=None,command_tp=None):
        msg = self.inner_data_wrapper(data,sender_type,recver_type,data_type,destination,command_tp)
        self.messagepool.put(msg)

    # 路由核心
    def routing(self):
        current_msg = self.messagepool.get(block=True)
        #commanding
        if current_msg['data_type'] == data['command'].value:
            # to central server
            if current_msg['optional']['command_type'] == command_type['login'].value:
                self.sok2server.Login(current_msg['data'])
            elif current_msg['optional']['command_type'] == command_type['logout'].value:
                self.sok2server.Logout(current_msg['data'])
                for subscriber in self._subscribers:
                    #need broadcast
                    subscriber.send(current_msg)
                    # self.detach(subscriber)
                self.working=False

            elif current_msg['optional']['command_type'] == command_type['query'].value:
                ipwanted = self.sok2server.GetIp(current_msg['data'])
                for subscriber in self._subscribers:
                    if subscriber.worker_type == worker_type['gui'].value:
                        subscriber.update_contacts(current_msg['data'],ipwanted)
            
            # to specific sender
            elif current_msg['optional']['command_type'] == command_type['hi'].value:
                for subscriber in self._subscribers:
                    if subscriber.desid == current_msg['optional']['destination']:
                        subscriber.send(current_msg)

            elif current_msg['optional']['command_type']==command_type['reject'].value:
                for subscriber in self._subscribers:
                    if subscriber.desid == current_msg['optional']['destination']:
                        subscriber.send(current_msg)
                        self.detach(subscriber)
                        break

            elif current_msg['optional']['command_type'] == command_type['establish'].value:
                hasEstablished = False
                for subscriber in self._subscribers:
                    if subscriber.desid == current_msg['optional']['destination']:
                        hasEstablished=True
                        break
                if not hasEstablished:
                    newsender = ChatSender()
                    newsender.address = current_msg['data']
                    newsender.port = LOCALPORT
                    newsender.srcid = self.myid
                    newsender.desid = current_msg['optional']['destination']
                    newsender.start()
                    self.attach(newsender)
            elif current_msg['optional']['command_type'] == command_type['disconnect'].value:#disconnect
                for subscriber in self._subscribers:
                    if subscriber.desid==current_msg['optional']['destination']:
                        subscriber.send(current_msg)
                        self.detach(subscriber)
            elif current_msg['data']==str(command_type['hi'].value):
                print("recv say hi!")
                for subscriber in self._subscribers:
                    if subscriber.worker_type == worker_type['gui'].value:
                        subscriber.send(current_msg)
            elif current_msg['data']==str(command_type['reject'].value):
                for subscriber in self._subscribers:
                    if subscriber.worker_type == worker_type['gui'].value:
                        subscriber.send(current_msg)

        # messaging
        else:
            if current_msg['recver_type']==worker_type['sender'].value:
                for subscriber in self._subscribers:
                    if subscriber.desid==current_msg['optional']['destination']:
                        subscriber.send(current_msg)
            
            elif current_msg['recver_type']==worker_type['gui'].value:
                # print(current_msg['data']) #send msg to gui
                for subscriber in self._subscribers:
                    if subscriber.worker_type == worker_type['gui'].value:
                        subscriber.send(current_msg)
        self.messagepool.task_done()

    #deprecated
    @contextmanager
    def subscribe(self, *tasks):
        for task in tasks:
            self.attach(task)
        
        try:
            yield
        finally:
            for task in tasks:
                self.detach(task)

    # 内部线程间数据报封装
    def inner_data_wrapper(self, data2trans, sender_type,recver_type,data_type,destination=None,command_tp=None):
        more = {
            'destination':None,
            'command_type':None
        }
        if recver_type == worker_type['sender'].value:
            more['destination']=destination
        if data_type == data['command'].value:
            more['command_type']=command_tp

        inner_data = {
            'sender_type':sender_type,
            'recver_type':recver_type,
            'data_type': data_type,
            'optional':more,
            'data':data2trans
        }
        return inner_data
from Chatter.data_type import *
from Chatter.listener import *
from Chatter.sender import *
import queue
from contextlib import contextmanager


class router(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.messagepool = queue.Queue()
        self._subscribers = set()

    def run(self):
        while True:
            self.routing()

    def attach(self, task):
        self._subscribers.add(task)

    def detach(self, task):
        self._subscribers.remove(task)

    def recv(self,data, sender_type,recver_type,data_type,destination=None):
        msg = self.inner_data_wrapper(data,sender_type,recver_type,data_type,destination)
        self.messagepool.put(msg)

    def routing(self):
        current_msg = self.messagepool.get(block=True)
        if current_msg['data_type'] == data['command'].value:
            # to central server
            if current_msg['data']['command_type'] == command_type['login'].value:
                for subscriber in self._subscribers:
                    if subscriber.desid == 0:
                        subscriber.login(current_msg['data'])
            elif current_msg['data']['command_type'] == command_type['logout'].value:
                for subscriber in self._subscribers:
                    if subscriber.desid == 0:
                        subscriber.logout(current_msg['data'])
            # to specific sender
            elif current_msg['data']['command_type'] == command_type['establish'].value:
                pass#TODO: 
            else:#disconnect
                for subscriber in self._subscribers:
                    if subscriber.desid==current_msg['optional']['destination']:
                        subscriber.send(current_msg)
                        self.detach(subscriber)

        else:
            if current_msg['recver_type']==worker_type['sender'].value:
                for subscriber in self._subscribers:
                    if subscriber.desid==current_msg['optional']['destination']:
                        subscriber.send(current_msg)
            
            elif current_msg['recver_type']==worker_type['gui'].value:
                print(current_msg['data']) #send msg to gui

    @contextmanager
    def subscribe(self, *tasks):
        for task in tasks:
            self.attach(task)
        
        try:
            yield
        finally:
            for task in tasks:
                self.detach(task)

    def inner_data_wrapper(self, data, sender_type,recver_type,data_type,destination=None):
        more = {}
        if recver_type == worker_type['sender'].value:
            more = {
                'destination':destination
            }

        inner_data = {
            'sender_type':sender_type,
            'recver_type':recver_type,
            'data_type': data_type,
            'optional':more,
            'data':data
        }
        return inner_data
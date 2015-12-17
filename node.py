#!/usr/bin/env python
#-*- coding=utf-8 -*-
#######################################################
#Author:    Zhanshuai Meng
#Created:   12 Dec 2015
#Version:   1.0
#######################################################

from multiprocessing import Process
from stateInfo import StateInfo
from message import Message
from collections import defaultdict
import socket
import threading
import os
import message
import tkinter as tk

try:
    import cPickle as pickle
except ImportError:
    import pickle

class Node(Process):
    def __init__(self,port=-1,ip_list=None,port_list=None,end_type=0,total_num,entry_num,exit_num):
        """
        end_type 0 is exit, 1 is entry

        """
        multiprocessing.Process.__init__(self)
        self.port = port
        self.ip_list = ip_list
        self.port_list = port_list
        self.ip = socket.gethostbyname(socket.gethostname())
        self.end_type = end_type
        self.state = StateInfo(total_num,entry_num,exit_num)
        self.counter = 0
        self.ack_critical = True
        self.update_flag = False # Wait fot the update reply from all other nodes
        self.isCoorn = False  # Not Coordinator
        self.inCritical = 0 #Not in critical region
        #self.message2send = []
        self.update_repley_procset = set()
        self.frame = tk.Tk()
        text = "Process "+str(os.getpid())
        button_text = ''
        if self.end_type == 0:
            text += ": exit:"
            button_text = 'Leave now'
        else:
            text += ": entry:"
            button_text = 'Enter now'
        self.frame.title(text)
        self.frame.geometry('400x300')
        self.text_plane = Text()
        self.text_plane.pack()
        Button(self.frame, text=button_text,command=self.update_pack).pack()
        Button(self.frame, text="State Info",command=self.get_state).pack()

    def set_coordinator(self):
        self.isCoorn = True
        self.cri_proc = None #who is in the critical region
        self.wait_queue = list()

    def sort_inser2waitqueue(self,message):
        if not self.wait_queue:
            self.wait_queue.append(message)
        elif self.wait_queue[0].timestamp > message.timestamp:
            self.wait_queue.insert(0,message)
        elif self.wait_queue[len(self.wait_queue)-1] < message.timestamp:
            self.wait_queue.append(message)
        else:
            for index in range(len(self.wait_queue)-1):
                if self.wait_queue[index].timestamp < message.timestamp and self.wait_queue[index+1] > message.timestamp:
                    self.wait_queue.insert(index,message)

    def send_message(self,ip,port,message):
        s = socket.socket(socket.AF_INEF, socket.SOCK_STREAM)
        s.connect((ip,port))
        data = pickle.dumps(message)
        s.send(data)
        s.close()

    def update_lamport_clock(self,message):
        data = message.data
        current_proc = os.getpid()
        source_proc = data[0]
        timestamp = data[1]
        #update clock
        self.counter = max(timestamp,self.counter)
        #increase VC


    def process_mess(self,sock,addr):
        data = sock.recv(1024)
        message = pickle.loads(data)
        update_lamport_clock(message)
        if message.mess_type == IN_TYPE or Message.mess_type == OUT_TYPE: # try to enter the critical
            if self.isCoorn: #Coordinator
                data = message.data
                pro_id = data[0]
                src_ip = data[2]
                src_port = data[3]
                if self.cri_proc and not self.cri_proc == pro_id: # wait
                    #sorted wait queue
                    self.sort_inser2waitqueue(message)
                else: # enter the critical region okay
                    self.cri_proc = pro_id
                    data = []
                    data.append(self.counter)
                    data.append(self.ip)
                    data.append(self.port)
                    ok_message = Message(ACK_REPLY_TYPE,self.stateInfo,data)
                    #self.message2send.append(ok_message)
                    self.send_message(src_ip,src_port,ok_message)

        elif message.mess_type == PARK_UPDATE_TYPE:
            stateInfo = message.state_info
            self.state = StateInfo(stateInfo.total_num,stateInfo.entry_num,stateInfo.exit_num)
            for index in range(len(self.ip_list)):
                data = []
                data.append(self.counter)
                data.append(self.ip)
                data.append(self.port)
                update_reply_message = Message(UPDATE_REPLY_TYPE,self.stateInfo,data)
                #self.message2send.append(ok_message)
                self.send_message(self.ip_list[index],self.port_list[index],update_reply_message)
            pass
        elif message.mess_type == ACK_REPLY_TYPE:# ACK of the
            self.ack_critical = True #OK ,can enter the critical region
            ##TBD
            self.update_park()
            #send the update type to other nodes
            for index in range(len(self.port_list)):
                if not self.port_list[index] == self.port:
                    data = []
                    data.append(self.counter)
                    data.append(self.ip)
                    data.append(self.port)
                    park_update_message = Message(PARK_UPDATE_TYPE,self.stateInfo,data)
                    self.send_message(self.ip_list[index],self.port_list[index],park_update_message)

            while True:
                if self.update_flag:
                    break
            self.ack_critical = False
        elif message.mess_type == LEAVE_TYPE: #release the critical region
            if self.isCoorn:
                if self.wait_queue:
                    message = self.wait_queue[len(self.wait_queue)-1]
                    wait_data = message.data
                    src_ip = wait_data.ip
                    src_port = wait_data.sort
                    data = []
                    data.append(self.counter)
                    data.append(self.ip)
                    data.append(self.port)
                    ok_message = Message(ACK_REPLY_TYPE,self.stateInfo,data)
                    #self.message2send.append(ok_message)
                    self.send_message(src_ip,src_port,ok_message)

        else: # mess_type == UPDATE_REPLY_TYPE:
            #nothing to be processed
            data = message.data
            self.update_repley_procset.add(data.pro_id)
            if len(self.update_repley_procset)==(len(self.port_list)-1): #exclude the process itself
                self.update_flag = True
        sock.close()

    def conn_proc(self,s):
        while(True):
            sock, addr = s.accept()
            t = threading.Thread(target=process_mess,args=(sock,addr))
            t.start()

    def change_state(self):
        if self.end_type == 0:
            pass
        else:
            pass
        pass

    def update_textplane(self,text):
        self.text_plane.insert(1.0,text)

    def get_state(self):
        text = "TOTAL_NUM: "+str(self.state.tatal_num)+", ENTRY_NUM: "+str(self.state.entry_num)+", EXIT_NUM: "+str(self.state.exit_num)
        self.update_textplane(text)
    def send2proc(self):



########Process Run **********************************8
    def run(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(self.ip,self.port)
        s.listen(5)
        t1 = threading.Thread(target=self.conn_proc,args=(sock,s))
        t1.start()
        #t2 = threading.Thread(target=self.send2proc)
        self.frame.mainloop()





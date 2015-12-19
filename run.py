#/usr/bin/env python
#-*- coding=utf-8 -*-
import sys
from stateInfo import *
from node import *
from message import *
import message
import time

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    print(len(sys.argv))
    if not len(sys.argv) == 4 or (not is_number(sys.argv[1]) and not is_number(sys.argv[2]) and not is_number(sys.argv[3])):
        print("Usage: python run.py TOTAL_NUM(int) ENTRY_NUM(int) EXIT_NUM(int) ")
        exit()
    total_num = int(sys.argv[1])
    entry_num = int(sys.argv[2])
    exit_num = int(sys.argv[3])
    port = 10003
    ip = 'localhost'
    port_list = []
    ip_list = []
    for i in range(entry_num+exit_num):
        port_list.append(port)
        port += 2
        ip_list.append(ip)
    for index,port in enumerate(port_list):
        if index<entry_num:
            p = Node(port,ip_list,port_list,1,total_num,entry_num,exit_num)
            #p.start()
        else:
            p = Node(port,ip_list,port_list,0,total_num,entry_num,exit_num)
            #p.start()











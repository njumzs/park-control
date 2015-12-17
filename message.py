#!/usr/bin/env python
#-*- coding=utf-8 -*-
######################################
#Author:    Zhanshuai Meng
#Created:   12 Dec 2015
#Version:   1.0
#######################################

# Message
## type
## stateinfo
## data
### pro_id
### timestamp
### ip
### port


from stateInfo import StateInfo

IN_TYPE = 1  #New car come in
OUT_TYPE = 2 #A car got out
PARK_UPDATE_TYPE = 3 # Broadcast to let other nodes update TOTAL_PARK
ACK_REPLY_TYPE = 4   #In or out reply
UPDATE_REPLY_TYPE = 5


class Message(object):
    def __init__(self,mess_type,stateInfo,data):
        self.mess_type = mess_type
        self.state_info = stateInfo
        self.data = data


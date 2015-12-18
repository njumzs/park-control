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

ASK_CRI_TYPE = 1  #New car come in or out
PARK_UPDATE_TYPE = 2 # Broadcast to let other nodes update TOTAL_PARK
ACK_REPLY_TYPE = 3   #In or out reply
REJECT_REPLY_TYPE = 4 #Critical is used and  wait
UPDATE_REPLY_TYPE = 5
RELEASE_TYPE = 6  #Leave the critical region

class Message(object):
    def __init__(self,mess_type,stateInfo,data):
        self.mess_type = mess_type
        self.state_info = stateInfo
        self.data = data


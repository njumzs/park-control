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


#from stateInfo import StateInfo



class MessageData:
    def __init__(self,mess_type,stateinfo,data):
        self.mess_type = mess_type
        self.state_info = stateinfo
        self.data = data


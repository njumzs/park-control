#!/usr/bin/env python
#-*- coding=utf-8 -*-
################################################################################
#Author:    Zhanshuai Meng
#Created:   Dec 12 2015
#Version:   1.0
################################################################################

class StateInfo(object):
    def __init__(self,total_num=5,entry_num=1,exit_num=1):
        self.total_num = total_num
        self.entry_num = entry_num
        self.exit_num = exit_num

    def decre_tatal_num(self,num):
        self.total_num -= num
        self.tatal_num = max(0,self.total_num)

    def incre_total_num(self,num):
        self.tatal_num += num

    def decre_entry_num(self,num):
        self.entry_num -= num
        self.entry_num = max(0,self.entry_num)

    def incre_entry_num(self,num):
        self.entry_num += num

    def decre_exit_num(self,num):
        self.exit_num -= num
        self.exit_num = max(0,self.exit_num)

    def incre_exit_num(self,num):
        self.exit_num += num

    def set_total_num(self,total_num):
        self.total_num = total_num

    def set_entry_num(self,entry_num):
        self.entry_num = entry_num

    def set_exit_num(slef,exit_num):
        self.exit_num = exit_num







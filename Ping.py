#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 17:23:32 2020

@author: hardikvachhani
"""


import os
hostname = "192.168.1.2"
response = os.system ("ping -c 5 " +hostname)
if response ==0:
    print(hostname, "is up")
else:
    print(hostname, "is down")
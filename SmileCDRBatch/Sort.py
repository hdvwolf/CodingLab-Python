#coding: utf8

import sys
import os
import json
import operator
import schedule
import requests

with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/Encounter.ndjson', 'r', encoding='latin-1') as E:
    #Read lines
    Edata = E.readlines()
    lines = []
    for x in Edata:
        json_obj = json.loads(x)
        lines.append(json_obj)
    lines = sorted(lines, key=lambda k: k['period']['start'], reverse=False)    
    lp = open("EncounterSorted.ndjson", "w")
    for line in lines:
        # print(line)
        jo = json.dumps(line)
        lp.write(jo) 
        lp.write('\r\n') 
    lp.close()


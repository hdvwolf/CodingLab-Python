# Python program to read Patinet, Encounter and Claims json file
#

import json
import requests
import schedule
import time

def BatchLoad():
    plist=[]
    elist=[]
    clist=[]
    # Tells how many lines to from Patient file in this session
    linestoload = 10000
    #Reading control json file which would tells where we left on last session
    control_file = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/ctrl.json", "r")
    #Reading File as Json
    json_object = json.load(control_file)
    #Closing File
    control_file.close()
    #Picking up value for tag linecounter
    last_line_read=json_object['linecounter']
    #Reading Patient.ndjson
    with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/Patient.ndjson', 'r', encoding='latin-1') as P:
        Pdata = P.readlines()
        #Reading Lines from range we want
        PatientData = Pdata[last_line_read:last_line_read+linestoload]
        # PatientData = Pdata[0:1]
        #Process loop for each line
        for x in PatientData:
            # w=open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/CurrentRecordCount.json','r')
            # linesread = json.load(w)
            # w.close()
            # lr = linesread['PatientRead']
            # linesread['PatientRead'] = lr+1
            # w=open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/CurrentRecordCount.json','w')
            # json.dump(linesread, w)
            # w.close()
            #Prepping header for service call
            headers = {"Accept":"application/json", "Content_Type":"application/json"}
            #Prepping payload for service
            data = x.encode('utf-8','ignore').decode('utf-8', 'replace')
            #Initiate service session
            s = requests.session()
            #Post....
            s.headers = headers = {'Accept': 'application/json','Content-Type': 'application/json'}
            http = s.post("http://sales-demo.smilecdr.com:18000/fhir-request/Patient", data)
            #Update log file with response Payload
            f = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/log.txt", "a")
            output=json.dumps(http.json(),indent=2)
            f.write(output)
            f.close()
            #Update tmp file with current record loaded
            lp = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/tmp.txt", "w")
            lp.write(x)
            lp.close()
            #Re-read tmp file to pickup identifier id
            l = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/tmp.txt","r")
            jo = json.load(l)
            l.close()
            pref=jo['id']
            #Load identifier of loaded Patient to PL.txt file 
            lp = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/PL.txt", "a")
            lp.write(pref)
            lp.write('\n')
            lp.close()
    # Incrementing Control File Count by lines to be loaded..
    json_object['linecounter'] = last_line_read + linestoload
    #Write Lines read in this session to Control File
    control_file = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/ctrl.json", "w")
    json.dump(json_object, control_file)
    control_file.close()

    #Start reading Encounter.ndjson
    with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/EncounterSorted.ndjson', 'r', encoding='latin-1') as E:
        #Read lines
        Edata = E.readlines()
        # EncounterData = Edata[last_line_read:last_line_read+linestoload]
        #For each line do following.....
        for x in Edata:
            # w=open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/CurrentRecordCount.json','r')
            # linesread = json.load(w)
            # w.close()
            # lr = linesread['EncounterRead']
            # linesread['EncounterRead'] = lr+1
            # w=open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/CurrentRecordCount.json','w')
            # json.dump(linesread, w)
            # w.close()
            #Prepare header for service call
            headers = {"Accept":"application/json", "Content_Type":"application/json"}
            data = x.encode('utf-8','ignore').decode('utf-8', 'replace')
            #Write record on hand to tmp
            lp = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/tmp.txt", "w")
            lp.write(x)
            lp.close()
            #Pick up id for current record
            l = open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/tmp.txt','r')
            jo = json.load(l)
            l.close()
            eref=jo['id']
            #Check if Patient reference record exists..
            with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/tmp.txt','r') as t:
                if '"subject": {"reference": "Patient/' in t.read():
                    pref=jo['subject']['reference']
                    #Strip patient reference from string...
                    matchstring=pref.strip('Patient/')
                    with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/PL.txt') as f:
                        #check if patient is already loaded if yes then proceed with calling service
                        if matchstring in f.read():
                            if eref not in open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/EL.txt","r").read():
                                s = requests.session()
                                s.headers = headers = {'Accept': 'application/json','Content-Type': 'application/json'}
                                http = s.post("http://sales-demo.smilecdr.com:18000/fhir-request/Encounter", data)
                                f = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/log.txt", "a")
                                output=json.dumps(http.json(),indent=2)
                                f.write(output)
                                f.close()
                                lp = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/EL.txt", "a")
                                lp.write(eref)
                                lp.write('\n')
                                lp.close()



    with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/Claim.ndjson', 'r', encoding='latin-1') as C:
        Cdata = C.readlines()
        # ClaimsData = Cdata[last_line_read:last_line_read+linestoload]
        for x in Cdata:
            # w=open('CurrentRecordCount.json','r')
            # linesread = json.load(w)
            # w.close()
            # lr = linesread['ClaimsRead']
            # linesread['ClaimsRead'] = lr+1
            # w=open('CurrentRecordCount.json','w')
            # json.dump(linesread, w)
            # w.close()
            headers = {"Accept":"application/json", "Content_Type":"application/json"}
            data = x.encode('utf-8','ignore').decode('utf-8', 'replace')
            lp = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/tmp.txt", "w")
            lp.write(x)
            lp.close()
            l = open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/tmp.txt','r')
            jo = json.load(l)
            l.close()
            cref=jo['id']
            pref=jo['patient']['reference']
            matchstring=pref.strip('Patient/')
            with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/PL.txt') as f:
                if matchstring in f.read():
                    if cref not in open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/CL.txt","r").read():
                        s = requests.session()
                        s.headers = headers = {'Accept': 'application/json','Content-Type': 'application/json'}
                        http = s.post("http://sales-demo.smilecdr.com:18000/fhir-request/Claim", data)
                        f = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/log.txt", "a")
                        output=json.dumps(http.json(),indent=2)
                        f.write(output)
                        f.close()
                        lp = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/CL.txt", "a")
                        lp.write(cref)
                        lp.write('\n')
                        lp.close()                            




schedule.every(0.5).minutes.do(BatchLoad)

while True:
    schedule.run_pending()
    time.sleep(0.5)

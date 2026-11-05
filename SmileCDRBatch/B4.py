# Python program to read Patinet, Encounter and Claims json file

import json
import requests
import schedule
import time

def BatchLoad():
    plist=[]
    prev=0
    linestoload = 10000
    control_file = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/ctrl.json", "r")
    json_object = json.load(control_file)
    control_file.close()
    last_line_read=json_object['linecounter']
    with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/Patient.ndjson', 'r', encoding='latin-1') as P:
        Pdata = P.readlines()
        PatientData = Pdata[last_line_read:last_line_read+linestoload]
        for x in PatientData:
            headers = {"Accept":"application/json", "Content_Type":"application/json"}
            data = x.encode('utf-8','ignore').decode('utf-8', 'replace')
            s = requests.session()
            s.headers = headers = {'Accept': 'application/json','Content-Type': 'application/json'}
            http = s.post("http://sales-demo.smilecdr.com:18000/fhir-request/Patient", data)
            f = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/log.txt", "a")
            output=json.dumps(http.json())
            f.write(output)
            f.close()
            jo = json.load(x.encode('utf-8','ignore').decode('utf-8', 'replace'))
            pref=jo['id']
            plist.append(pref)

    json_object['linecounter'] = last_line_read + linestoload
    control_file = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/ctrl.json", "w")
    json.dump(json_object, control_file)
    control_file.close()

    with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/EncounterSorted.ndjson', 'r', encoding='latin-1') as E:
        Edata = E.readlines()
        for x in Edata:
            headers = {"Accept":"application/json", "Content_Type":"application/json"}
            data = x.encode('utf-8','ignore').decode('utf-8', 'replace')
            jo = json.load(x.encode('utf-8','ignore').decode('utf-8', 'replace'))
            eref=jo['id']
            pref=jo['subject']['reference']
            matchstring=pref.strip('Patient/')
            if prev == matchstring:   
                s = requests.session()
                s.headers = headers = {'Accept': 'application/json','Content-Type': 'application/json'}
                http = s.post("http://sales-demo.smilecdr.com:18000/fhir-request/Encounter", data)
                f = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/log.txt", "a")
                output=json.dumps(http.json())
                f.write(output)
                f.close()
            elif matchstring in plist:
                prev=matchstring
                s = requests.session()
                s.headers = headers = {'Accept': 'application/json','Content-Type': 'application/json'}
                http = s.post("http://sales-demo.smilecdr.com:18000/fhir-request/Encounter", data)
                f = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/log.txt", "a")
                output=json.dumps(http.json())
                f.write(output)
                f.close()
                
    with open('/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/Claim.ndjson', 'r', encoding='latin-1') as C:
        Cdata = C.readlines()
        for x in Cdata:
            headers = {"Accept":"application/json", "Content_Type":"application/json"}
            data = x.encode('utf-8','ignore').decode('utf-8', 'replace')
            jo = json.load(x.encode('utf-8','ignore').decode('utf-8', 'replace'))
            cref=jo['id']
            pref=jo['patient']['reference']
            matchstring=pref.strip('Patient/')
            if prev == matchstring:   
                s = requests.session()
                s.headers = headers = {'Accept': 'application/json','Content-Type': 'application/json'}
                http = s.post("http://sales-demo.smilecdr.com:18000/fhir-request/Encounter", data)
                f = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/log.txt", "a")
                output=json.dumps(http.json())
                f.write(output)
                f.close()                
            elif matchstring in plist:
                prev=matchstring
                s = requests.session()
                s.headers = headers = {'Accept': 'application/json','Content-Type': 'application/json'}
                http = s.post("http://sales-demo.smilecdr.com:18000/fhir-request/Claim", data)
                f = open("/Users/hardikvachhani/Documents/GitHub/L1C/SmileCDRBatch/log.txt", "a")
                output=json.dumps(http.json())
                f.write(output)
                f.close()

schedule.every(0.5).minutes.do(BatchLoad)

while True:
    schedule.run_pending()
    time.sleep(0.5)

# Python program to read Patinet, Encounter and Claims json file

import json
import requests
import schedule
import time

def BatchLoad():
    PatientFilePath="/Downloads/SmileCDRBatch/Patient.ndjson"
    EnconterFilePath="/Downloads/SmileCDRBatch/EncounterSorted.ndjson"
    ClaimsFilePath="/Downloads/SmileCDRBatch/Claim.ndjson"
    LogFilePath="/Users/kishorekulkarni/Downloads/SmileCDRBatch/log.txt"
    ControlFilePath="/Users/kishorekulkarni/Downloads/SmileCDRBatch/ctrl.json"
    PBaseURL="http://localhost:8000/Patient"
    EBaseURL="http://localhost:8000/Encounter"
    CBaseURL="http://localhost:8000/Claim"
    headers = {'Accept': 'application/json','Content-Type': 'application/json'}
    plist=[]
    linestoload = 15000
    control_file = open(ControlFilePath, "r")
    json_object = json.load(control_file)
    control_file.close()
    last_line_read=json_object['linecounter']
    with open(PatientFilePath, 'r', encoding='latin-1') as P:
        Pdata = P.readlines()
        PatientData = Pdata[last_line_read:last_line_read+linestoload]
        for x in PatientData:
            headers = {"Accept":"application/json", "Content_Type":"application/json"}
            data = x.encode('utf-8','ignore').decode('utf-8', 'replace')
            s = requests.session()
            s.headers = headers = {'Accept': 'application/json','Content-Type': 'application/json'}
            http = s.post(PBaseURL, data)
            f = open(LogFilePath, "a")
            # if http.status_code != 201:
            #     exit()
            output=json.dumps(http.json())
            f.write(output)
            f.close()
            lp = open("tmp.txt", "w")
            lp.write(x)
            lp.close()
            l = open("tmp.txt","r")
            jo = json.load(l)
            l.close()
            pref=jo['id']
            plist.append(pref)

    json_object['linecounter'] = last_line_read + linestoload
    control_file = open(ControlFilePath, "w")
    json.dump(json_object, control_file)
    control_file.close()

    with open(EnconterFilePath, 'r', encoding='latin-1') as E:
        Edata = E.readlines()
        for x in Edata:
            headers = {"Accept":"application/json", "Content_Type":"application/json"}
            data = x.encode('utf-8','ignore').decode('utf-8', 'replace')
            lp = open("tmp.txt", "w")
            lp.write(x)
            lp.close()
            l = open("tmp.txt","r")
            jo = json.load(l)
            l.close()
            eref=jo['id']
            pref=jo['subject']['reference']
            matchstring=pref.strip('Patient/')
            if matchstring in plist:
                s = requests.session()
                s.headers = headers 
                http = s.post(EBaseURL, data)
                f = open(LogFilePath, "a")
                # if http.status_code != 201:
                #     exit()
                output=json.dumps(http.json())
                f.write(output)
                f.close()
                
    with open(ClaimsFilePath, 'r', encoding='latin-1') as C:
        Cdata = C.readlines()
        for x in Cdata:
            headers = {"Accept":"application/json", "Content_Type":"application/json"}
            data = x.encode('utf-8','ignore').decode('utf-8', 'replace')
            lp = open("tmp.txt", "w")
            lp.write(x)
            lp.close()
            l = open("tmp.txt","r")
            jo = json.load(l)
            l.close()
            cref=jo['id']
            pref=jo['patient']['reference']
            e=[]
            itemlistvalue=[]
            itemlist=[]
            aindent=0
            bindent=0
            for y in jo['item']:
                itemlist.append(jo['item'][aindent])
                aindent=aindent+1
            for y in itemlist:
                itemlistvalue=itemlist[bindent]
                bindent=bindent+1
                if "encounter" in itemlistvalue:
                    encounterlist=itemlistvalue['encounter']
                    z=0
                    for w in encounterlist:
                        encounters=encounterlist[z]
                        z=z+1     
                        eref=encounters['reference']
                        matchstring=pref.strip('Patient/')
                        matchstring1=eref.strip('Encounter/')
                        purl=PBaseURL + "?identifier=" + matchstring
                        eurl=EBaseURL + "?identifier=" + matchstring1
                        if requests.get(purl).status_code == 200:
                            if requests.get(eurl).status_code == 200:                   
                                s = requests.session()
                                s.headers = headers 
                                http = s.post("http://localhost:8000/Claim", data)
                                f = open(LogFilePath, "a")
                                output=json.dumps(http.json())
                                f.write(output)
                                f.close()
                                # if http.status_code != 201:
                                #     exit()
                else:
                    matchstring=pref.strip('Patient/')
                    purl="http://localhost:8000/Patient" + matchstring
                        
                    if requests.get(purl).status_code == 200:                    
                            s = requests.session()
                            s.headers = headers 
                            http = s.post(CBaseURL, data)
                            f = open(LogFilePath, "a")
                            output=json.dumps(http.json())
                            f.write(output)
                            f.close()
                            # if http.status_code != 201:
                            #     exit()

schedule.every(0.5).minutes.do(BatchLoad)

while True:
    schedule.run_pending()
    time.sleep(0)

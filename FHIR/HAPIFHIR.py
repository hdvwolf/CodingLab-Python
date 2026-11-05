import json
import requests
import xml.etree

#def jprint(obj):
   # create a formatted string of the Python JSON object
#    text = json.dumps(obj, sort_keys=False, indent=20)
 #   print(text)

header={'Content-Type':'application/JSON'}

f = open("metadata.txt", "w")

finput=open("inputJSON.txt", "r")
foutput=open("outputJSON.txt","w")
parameters=finput.read()
#parameters=parameters.tojson()
request1 =  requests.put("http://hapi.fhir.org/baseR4/Patient/1475248", headers=header, data=parameters)
foutput.write(json.dumps(request1.json(), sort_keys=False, indent=4))

finput.close()
foutput.close()

#jprint(pass_times)
#risetimes = []
#for d in pass_times:
#    time = d['risetime']
#    risetimes.append(time)

#test
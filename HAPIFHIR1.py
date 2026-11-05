#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 19:25:24 2020

@author: hardikvachhani
"""

import json
import requests


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

f = open("HAPIFHIRmetadata.json", "w")
response1 = requests.get("http://hapi.fhir.org/baseR4/metadata/")
#print(response1.status_code)
#jprint(response1.json())
output=json.dumps(response1.json(), sort_keys=True, indent=4)
f.write(output)
f.close()

f = open("HAPIFHIRPatient.json", "w")
response1 = requests.get("http://hapi.fhir.org/baseR4/Patient/")
#print(response1.status_code)
#jprint(response1.json())
output=json.dumps(response1.json(), sort_keys=True, indent=4)
f.write(output)
f.close()

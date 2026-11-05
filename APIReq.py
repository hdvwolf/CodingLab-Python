


import json
import requests

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
response1 = requests.get("http://api.open-notify.org/iss-now.json")
#print(response1.status_code)
print("Where is ISS right now?")
#print(response1.json())
IssLoc = response1.json()['iss_position']
print(IssLoc)
print("\n")

# response2 = requests.get("http://api.open-notify.org/astros.json")
# #print(response2.status_code)
# #jprint(response2.json())
# IssAstronuats = response2.json()['people']
# astronauts=[]
# for astro in IssAstronuats:
#     temp1 = astro['name']
#     astronauts.append(temp1)
# print('Who all are present on ISS today?')
# print(astronauts)
# print("\n")
#
# #Lattitude and Logitudes where you need Viewing Time schedule
# YourLat = input("Please enter Lattitude ISS viewing scheude is needed for:\n")
# YourLong = input("Please enter Longitude ISS viewing scheude is needed for:\n")
# parameters = {
#     "lat": YourLat,
#     "lon": YourLong
# }
# print("Location ISS viewing schedule is needed is - {}".format(parameters))
# response3 = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
# #print(response3.status_code)
# #jprint(response3.json())
# pass_times = response3.json()['response']
# #jprint(pass_times)
# risetimes = []
# for d in pass_times:
#     time = d['risetime']
#     risetimes.append(time)
# #print(risetimes)
# from datetime import datetime
# times = []
# print("\nISS viewing Schedule where your coordinates are\n")
# for rt in risetimes:
#     time = datetime.fromtimestamp(rt)
#     times.append(time)
#     print(time)

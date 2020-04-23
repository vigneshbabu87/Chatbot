# thisdict = {'error': False, 'statusCode': 200, 'message': 'OK',
#          'data':
#               {'recovered': 3975, 'deaths': 645, 'confirmed': 20080,
#               'lastChecked': '2020-04-22T09:54:08+00:00', 'lastReported': '2020-04-21T23:30:30+00:00',
#              'location': 'India'}
#        }

# print(thisdict['data']['recovered'])

path=app.instance_path
print(path)

thisdictnew = {
    "Message": "Number of Post office(s) found: 7",
    "Status": "Success",
    "PostOffice": [
        {
            "Name": "Chennai ",
            "Description": "",
            "BranchType": "Head Post Office",
            "DeliveryStatus": "Delivery",
            "Taluk": "Chennai",
            "Circle": "Chennai",
            "District": "Chennai",
            "Division": "Chennai GPO",
            "Region": "Chennai Region",
            "State": "Tamil Nadu",
            "Country": "India"
        }
    ]
}

print(thisdictnew['PostOffice'][0]['District'])
print(thisdictnew['PostOffice'][0]['State'])


# get dsitrict details

getdistrictdata=[
    {
        "state": "Andaman and Nicobar Islands",
    "statecode": "AN",
    "districtData": [
      {
        "district": "North and Middle Andaman",
        "notes": "",
        "active": 0,
        "confirmed": 1,
        "deceased": 0,
        "recovered": 1,
        "delta": {
          "confirmed": 0,
          "deceased": 0,
          "recovered": 0
        }
      },
      {
        "district": "South Andaman",
        "notes": "",
        "active": 6,
        "confirmed": 16,
        "deceased": 0,
        "recovered": 10,
        "delta": {
          "confirmed": 1,
          "deceased": 0,
          "recovered": 0
        }
      },
      {
        "district": "Unknown",
        "notes": "",
        "active": 1,
        "confirmed": 1,
        "deceased": 0,
        "recovered": 0,
        "delta": {
          "confirmed": 0,
          "deceased": 0,
          "recovered": 0
        }
      }
    ]
  },
    {
        "state": "Andhra Pradesh",
        "statecode": "AP",
        "districtData": [
            {
                "district": "Anantapur",
                "notes": "",
                "active": 31,
                "confirmed": 36,
                "deceased": 3,
                "recovered": 2,
                "delta": {
                    "confirmed": 0,
                    "deceased": 0,
                    "recovered": 0
                }
            }]
    },
{
    "state": "Tamil Nadu",
    "statecode": "TN",
    "districtData": [
      {
        "district": "Ariyalur",
        "notes": "",
        "active": 5,
        "confirmed": 5,
        "deceased": 0,
        "recovered": 0,
        "delta": {
          "confirmed": 2,
          "deceased": 0,
          "recovered": 0
        }
      }]
}
]

print(getdistrictdata[0]['districtData'])
index=0
state="Tamil Nadu"

for statedet in getdistrictdata:
    print(statedet)
    if(statedet['state']==state):#"Andhra Pradesh"):
        for val in getdistrictdata[index]['districtData']:
            print(val['district'])
            if(val['district']=="Ariyalur"):
                print(val['confirmed'])
                confirm=int(val['confirmed']) + int(val['delta']['confirmed'])
                print(confirm)
    index=index+1

print(getdistrictdata[0]['districtData'][1]['district'])


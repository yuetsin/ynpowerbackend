import requests
import json


def getData(location, dataName, startTime, endTime):
    l = location.split("_")
    url = 'https://ynpowerbackend.dclab.club/getDataJson'

    s = json.dumps({
        "dataName": dataName,
        "startTime": startTime,
        "endTime": endTime,
        "grain": l[1],
        "area": l[0],
        "kind": l[2]
    })

    r = requests.post(url, data=s, headers={'Content-Type': 'application/json'}, verify=False)
    #print(r.json())
    return r.json()

if __name__ == '__main__':
    r = getData("yunnan_year_社会经济类", "GDP1", "2008", "2016")
    re = json.loads(r)
    print(re)
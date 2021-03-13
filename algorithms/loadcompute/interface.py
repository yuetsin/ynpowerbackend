import requests
import json
from datetime import datetime

host = "http://dclab.club:18000/"

def getData(location, dataName, startTime, endTime):
    l = location.split("_")
    # url = 'http://ynpowerbackend.dclab.club/getDataJson'
    url = host + 'getDataJson'
    startTime = formateTimeString(startTime, l[1])
    endTime = formateTimeString(endTime, l[1])
    s = json.dumps({
        "dataName": dataName,
        "startTime": startTime,
        "endTime": endTime,
        "grain": l[1],
        "area": l[0],
        "kind": l[2]
    })

    r = requests.post(url, data=s, headers={'Content-Type': 'application/json'}, verify=False)
    # print(r)
    return r.json()
def insertAlgorithmResult(tag, result):

    # url = 'http://ynpowerbackend.dclab.club/api/insert/result'
    url = host + 'api/insert/result'
    s = json.dumps({
        "result": result,
        "tag": tag
    })

    r = requests.post(url, data=s, headers={'Content-Type': 'application/json'}, verify=False)
    #print(r.json())
    return r.json()



#"tags":"tv1,tv2", 是一个字符串
def getAlgorithmResult(tags):

    # url = 'http://ynpowerbackend.dclab.club/api/get/result'
    url = host + '/api/get/result'
    s = json.dumps({
        "tags": tags
    })

    r = requests.post(url, data=s, headers={'Content-Type': 'application/json'}, verify=False)
    #print(r.json())
    return r.json()

def formateTimeString(t, grain):
    if grain == 'day':
        timet = datetime.strptime(t, '%Y/%m/%d')
        timestr = timet.strftime('%Y/%m/%d')
    elif grain == 'mouth':
        timet = datetime.strptime(t, '%Y/%m')
        timestr = timet.strftime('%Y/%m')
    elif grain == 'hour':
        timet = datetime.strptime(t, '%Y/%m/%d %H')
        timestr = timet.strftime('%Y/%m/%d %H')
    elif grain == 'min':
        timet = datetime.strptime(t, '%Y/%m/%d %H:%M')
        timestr = timet.strftime('%Y/%m/%d %H:%M')
    elif grain == 'sec':
        timet = datetime.strptime(t, '%Y/%m/%d %H:%M:%S')
        timestr = timet.strftime('%Y/%m/%d %H:%M:%S')
    # print(timestr)
    return timestr

if __name__ == '__main__':
    # r = getData("yunnan_year_社会经济类", "GDP1", "2008", "2016")
    # re = json.loads(r)
    # print(re)
    # r = getAlgorithmResult("tv1,tv2")
    # re = json.loads(r)
    # print(re)
    # from algorithms.GM import GM
    # StartYear = "1990"
    # EndYear = "2019"
    # PreStartYear = "2020"
    # PreEndYear = "2029"
    # timestep = 15
    # pretype = "consumption"
    # result = GM(StartYear, EndYear, PreStartYear, PreEndYear, timestep, pretype="consumption")
    # # content = {}
    # # content['arg'] = {
    # #     "StartYear" : "1990",
    # #     "EndYear" : "2019",
    # #     "PreStartYear" : "2020",
    # #     "PreEndYear" : "2029",
    # #     "timestep" : 15,
    # #     "pretype" : "consumption"
    # # }
    # # content['result'] = result
    # # print(result)
    # r = insertAlgorithmResult("tv3", result)
    # print(r)
    # r = getAlgorithmResult("tv3")
    # re = json.loads(r)
    # tag = re['results'][0][0]
    # content = json.loads(re['results'][0][1])
    # print(type(content))
    # print(content['trainfromyear'])
    result = getData("yunnan_day_电力电量类", "N00_00", "2013/1/1", "2013/1/3")
    print(result)

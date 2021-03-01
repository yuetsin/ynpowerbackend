import requests
import json
from datetime import datetime
import pandas as pd
import numpy as np

# host = "http://dclab.club:18000/"
host = "http://localhost:5000/"

def getData(location, dataName, startTime, endTime):
    l = location.split("_")
    # url = 'http://ynpowerbackend.dclab.club/getDataJson'
    url = host + 'getDataJson'
    # startTime = formateTimeString(startTime, l[1])
    # endTime = formateTimeString(endTime, l[1])
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
    else:
        timet = datetime.strptime(t, '%Y')
        timestr = timet.strftime('%Y')
    # print(timestr)
    return timestr

if __name__ == '__main__':
    r = getData("yunnan_year_社会经济类-test", "GDP1", "2008", "2016")
    re = json.loads(r)
    print(re)
    # r = getAlgorithmResult("tv1,tv2")
    # re = json.loads(r)
    # print(re)
    # from algorithms.GM import GM
    # from  utils.tools import getAlgorithm
    # StartYear = "1990"
    # EndYear = "2019"
    # PreStartYear = "2020"
    # PreEndYear = "2029"
    # timestep = 15
    # pretype = "consumption"
    # f = getAlgorithm("GM")
    # result1 = f(StartYear, EndYear, PreStartYear, PreEndYear, timestep, pretype="consumption")
    # result2 = GM(StartYear, EndYear, PreStartYear, PreEndYear, timestep, pretype="consumption")
    # content = {}
    # content['arg'] = {
    #     "StartYear" : "1990",
    #     "EndYear" : "2019",
    #     "PreStartYear" : "2020",
    #     "PreEndYear" : "2029",
    #     "timestep" : 15,
    #     "pretype" : "consumption"
    # }
    # content['result'] = result
    # print(result1)
    # print(result2)
    # r = insertAlgorithmResult("tv3", result)
    # print(r)
    # r = getAlgorithmResult("tv3")
    # re = json.loads(r)
    # tag = re['results'][0][0]
    # content = json.loads(re['results'][0][1])
    # print(type(content))
    # print(content['trainfromyear'])
    result = getData("yunnan_day_电力电量类-测试1", None, "2013/1/1", "2013/1/3")
    print(result)
    # data  = pd.read_excel("./args.xlsx", None, index_col = None)
    # args = {}
    # for row in data.values():
    #     # print(row)
    #     x,y= row.shape
    #     header = [i for i in row.columns]
    #     for j in range(1, y):
    #         args[header[j]] = {
    #             "name": row.iloc[0][j],
    #         }
    #         count = 0
    #         for i in range(1, x):
    #             if row.iloc[i][0] != row.iloc[i][0] or row.iloc[i][j] != row.iloc[i][j]:
    #                 break
    #             if i % 2 == 0:
    #                 count += 1
    #                 continue
    #             args[header[j]][row.iloc[i][j]] = row.iloc[i+1][j]
    #         args[header[j]]["num"] = count
    #
    #
    # print(args)
        # print(row.shape)
        # for i, r in row.iterrows():
        #     print(r)

    # print(data)



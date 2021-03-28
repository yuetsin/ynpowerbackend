# from dao.interface import getDataByCondition, modifyDataByCondition, getTagByKind, getAllTag, renameTag, deleteTag, \
#     checkTag, insertAlgorithmContent, getGrain, getKind, getArea
from algorithms.Outlier import Outlier
from algorithms.loadcompute.default import default_jiabi, default_souku, default_f
from algorithms.loadcompute.main import dayFeature, monthFeature, yearfeature, yearLoad, dayLoad, typicalDay, \
    yearLoadCon
from algorithms.loadcompute.pre_process import d_pre_character
from algorithms.loadpredict.fenxing.fenxing import fenxingpre
from algorithms.loadpredict.shuangxiangjiabi.shuangxiangjiabi import shuangxiangjiabi
from algorithms.loadpredict.souku.souku import soukupre
from algorithms.loadpredict.zhishupinghua.zhishupinghua import zhishupinghua
from dao import *
from utils import *
import json


def exceptQuery(category, startTime, endTime, grain, area):
    data = getDataByCondition(grain = grain, startTime = startTime, endTime = endTime, kind = category[0], dataName = category[1], area = area)
    datalist = []
    grain1 = ['年', '月', '日', '时']
    grain2 = ["year", "month", "day", "hour"]
    for i in range(len(grain2)):
        if grain2[i] == grain:
            grain = grain1[i]
            break
    if data is not None:
        out = Outlier(StartYear=startTime, EndYear = endTime, pretype= category[1])
        if out["outlier"] == None:
            for d in data:
                temp = {}
                temp["key"] = d[0]
                temp["category"] = category
                temp['region'] = area
                temp['grain'] = grain
                temp['value'] = d[2]
                temp["suggest"] = out["correction"]
                datalist.append(temp)
    else:
        return None
    result = datalist
    return result

def exceptResolve(originData, modifiedData):
    grain = originData['grain']
    startTime = originData['key']
    endTime = originData['key']
    kind =  originData['category'][0]
    dataName = originData['category'][1]
    area = originData['region']
    grain1 = ['年', '月', '日', '时']
    grain2 = ["year", "month", "day", "hour"]
    for i in range(len(grain2)):
        if grain1[i] == grain:
            grain = grain2[i]
            break
    metadata = getMetaData(area, kind, grain)
    # print(metadata)
    metadataId = metadata[0][0]
    re = modifyDataByCondition(modifiedData['value'], startTime=startTime, endTime=endTime,
                               dataName=dataName, metadataid=metadataId)

    return re

def exceptAccept(originData):
    grain = originData['grain']
    startTime = originData['key']
    endTime = originData['key']
    kind = originData['category'][0]
    dataName = originData['category'][1]
    area = originData['region']
    suggest = originData["suggest"]
    grain1 = ['年', '月', '日', '时']
    grain2 = ["year", "month", "day", "hour"]
    for i in range(len(grain2)):
        if grain1[i] == grain:
            grain = grain2[i]
            break
    metadata = getMetaData(area, kind, grain)
    metadataId = metadata[0][0]
    if type(suggest) is not int:
        return {
            "msg":"无效建议值",
            "code": -1
        }

    re = modifyDataByCondition(suggest, startTime=startTime, endTime=endTime,
                               dataName=dataName, metadataid=metadataId)

    return re


def tagsQuery(tagType = None):
    if tagType != None:
        re = getTagByKind(tagType)
    else:
        re = getAllTag()
    return re

def tagsRename(current_name, new_name):
    current = checkTag(current_name)
    new = checkTag(new_name)
    if new:
        return {
                "msg": "key existed",
                "code": -1
            }
    elif current == False:
        return {
            "msg": "no key found",
            "code": -1
        }
    else:
        return renameTag(current_name, new_name)

def tagDelete(current_name):
    return deleteTag(current_name)

def miningRequest(tag, tagType, region, factors, method, arg, beginYear, endYear, args):
    # data = getDataByCondition(grain=None, startTime=str(beginYear), endTime=str(endYear), kind=None, dataName=None,
    #                           area=region)  # 是否需要粒度，和kind，dataname
    # f = getAlgorithm(method)
    # result = None
    # if method == "Pearson":
    #     threshold = arg['threshold']
    #     result = f()
    # elif method == "KMeans":
    #     suggestCategoryCount = arg['suggestCategoryCount']
    #     categoryCount = arg['categoryCount']
    #     result = f()
    # elif method == "PCA":
    #     absThreshold = arg['absThreshold']
    #     result = f()
    # elif method == "ARL":
    #     minSupport = arg['minSupport']
    #     minConfidence = arg['minConfidence']
    #     result = f()
    # (tag, tagType, region, factors, method, pearson, beginYear, endYear)
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    result = executeAlgorithm(method, args)
    content = {}
    content['arg'] = args
    content['result'] = result
    re = insertAlgorithmContent(tag, tagType, content)

    return result


def regionSinglePredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    result = executeAlgorithm(method, args)
    print(result)

    content = {}
    content['arg'] = args
    content["result"] = result
    re = insertAlgorithmContent(tag, tagType, content)
    result = formatPredictResult(result)
    print(result)
    return result

def regionMixPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    singleresult = []
    for tag in args["singleresult"]:
        result = getAlgorithmContentByTag(tag)

        singleresult.append(json.loads(result[0]["content"])["result"])
    args["singleresult"] = singleresult
    result = executeAlgorithm(method, args)

    content = {}
    content['arg'] = args
    content["result"] = result

    re = insertAlgorithmContent(tag, tagType, content)
    result = formatPredictResult(result)
    print(result)
    return result


def industrySinglePredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    result = executeAlgorithm(method, args)

    content = {}
    content['arg'] = args
    content["result"] = result

    re = insertAlgorithmContent(tag, tagType, content)
    result = formatPredictResult(result)
    print(result)
    return result

def industryMixPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    singleresult = []
    for tag in args["singleresult"]:
        result = getAlgorithmContentByTag(tag)

        singleresult.append(json.loads(result[0]["content"])["result"])
    args["singleresult"] = singleresult
    result = executeAlgorithm(method, args)
    content = {}
    content['arg'] = args
    content["result"] = result

    re = insertAlgorithmContent(tag, tagType, content)
    result = formatPredictResult(result)
    print(result)
    return result

def saturationCurvePredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    result = executeAlgorithm(method, args)

    content = {}
    content['arg'] = args
    content["result"] = result

    re = insertAlgorithmContent(tag, tagType, content)
    result = formatPredictResult(result)
    print(result)
    return result

def payloadDensityPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    result1 = executeAlgorithm(method, args)
    content = {}
    content['arg'] = args
    content["result"] = result1

    re = insertAlgorithmContent(tag, tagType, content)
    result = formatPredictResult(result1)
    result["bu"] = result1["bu"]
    print(result)

    return result


def provincialAndMunicipalPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)

    # provPlan = args['provPlan'] # 如果设置为 `__byUpload__` 则从上传文件中读取
    # provFile = args['provFile']  # 如果 provPlan 是 __byUpload__，那么从这里读
    # muniData  = args['muniData']
    result = executeAlgorithm(method, args)

    print(result)


    # content = {}
    # content['arg'] = args
    # content["result"] = result
    #
    # re = insertAlgorithmContent(tag, tagType, content)
    return result

def bigDataPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    result = executeAlgorithm(method, args)
    tableTwoData = []
    prefromyear = timeFormat(result["prefromyear"], "year")
    pretoyear = timeFormat(result["pretoyear"], "year")
    i = 0
    while prefromyear <= pretoyear:
        temp = {
            'year': prefromyear.strftime("%Y"),
            'predict': result['preresult'][i]
        }
        tableTwoData.append(temp)
        i += 1
        prefromyear = getNextYear(prefromyear)
    result = {
        "tableTwoData": tableTwoData
    }
    print(result)
    content = {}
    content['arg'] = args
    content["result"] = result

    re = insertAlgorithmContent(tag, tagType, content)

    return result

def dailyPayloadTraits(args):
    beginDay = args["beginDay"]
    endDay = args["endDay"]
    begin = timeFormat(beginDay, "day")
    end = timeFormat(endDay, "day")
    t1 = begin.strftime('%Y/%m/%d')
    t2 = end.strftime('%Y/%m/%d')
    result = dayFeature(t1, t2)
    # print(result)
    # result = []
    # while begin <= end:
    #     t = begin.strftime('%Y/%m/%d')
    #     temp = dayFeature(start=t, end=t)
    #     temp["day"] = t
    #     result.append(temp)
    #     begin = getNextDay(begin)



    # content = {}
    # content['arg'] = args
    # content["result"] = result
    #
    # re = insertAlgorithmContent(tag, tagType, content)

    return result

def monthlyPayloadTraits(args):
    beginMonth = args["beginMonth"]
    endMonth = args["endMonth"]

    begin = timeFormat(beginMonth, "month")
    end = timeFormat(endMonth, "month")
    end = getEndMonth(end)

    result = monthFeature(begin.strftime('%Y/%m/%d'), end.strftime("%Y/%m/%d"))
    # result = []
    # while begin <= end:
    #     t = begin.strftime('%Y/%m/%d')
    #     te = getEndMonth(begin)
    #     te = te.strftime("%Y/%m/%d")
    #     temp = monthFeature(start=t, end=te)
    #     temp["month"] = begin.strftime("%Y/%m")
    #     result.append(temp)
    #     begin = getNextMonth(begin)



    # content = {}
    # content['arg'] = args
    # content["result"] = result
    #
    # re = insertAlgorithmContent(tag, tagType, content)

    return result
def yearlyPayloadTraits(args):
    beginYear = args["beginYear"]
    endYear = args["endYear"]

    begin = timeFormat(beginYear, "year")
    end = timeFormat(endYear, "year")
    end = getEndYear(end)
    # result = []
    result = yearfeature(begin.strftime('%Y/%m/%d'), end.strftime('%Y/%m/%d'))
    # while begin <= end:
    #     t = begin.strftime('%Y/%m/%d')
    #     te = getEndYear(begin)
    #     te = te.strftime("%Y/%m/%d")
    #     temp = yearfeature(start=t, end=te)
    #     temp["year"] = begin.strftime("%Y")
    #     result.append(temp)
    #     begin = getNextYear(begin)


    # content = {}
    # content['arg'] = args
    # content["result"] = result
    #
    # re = insertAlgorithmContent(tag, tagType, content)

    return result


def sokuPayloadPredict(args):
    start = args["beginYear"]
    ending = args["endYear"]
    premaxload = args["maxPayload"]
    pretotal = args["dailyAmount"]
    pregamma = args["gamma"]
    prebeta = args["beta"]
    season = args["season"]
    t = args["type"]
    file = getFilenameOfLoadPre(season, t, "sk")
    result = soukupre(start, ending, premaxload, pretotal,pregamma,prebeta, file=file)
    tag = args["tag"]
    tagType = args["tagType"]
    content = {}
    content['arg'] = args
    content["result"] = result

    re = insertAlgorithmContent(tag, tagType, content)

    return content


def clampingPayloadPredict(args):
    start = args["beginYear"]
    ending = args["endYear"]
    premaxload = args["maxPayload"]
    pretotal = args["dailyAmount"]
    season = args["season"]
    t = args["type"]
    file = getFilenameOfLoadPre(season, t, "jb")
    result = shuangxiangjiabi(start, ending, premaxload, pretotal,file=file)
    tag = args["tag"]
    tagType = args["tagType"]
    content = {}
    content['arg'] = args
    content["result"] = result

    re = insertAlgorithmContent(tag, tagType, content)

    return content


def interpolatingPayloadPredict(args):
    start = args["beginYear"]
    ending = args["endYear"]
    power = args["dailyAmount"]
    maxload = args["maxPayload"]
    season = args["season"]
    t = args["type"]
    file = getFilenameOfLoadPre(season, t, "fx")
    result = fenxingpre(start, ending, power,maxload, file=file)
    tag = args["tag"]
    tagType = args["tagType"]
    content = {}
    content['arg'] = args
    content["result"] = result
    re = insertAlgorithmContent(tag, tagType, content)

    return content

def yearlyContinuousPayloadPredict(args):
    start = str(args["beginYear"])
    end = str(args["endYear"])
    premaxload = args["maxPayload"]
    endyear = timeFormat(end, "year")
    Tyear = getNextYear(endyear)
    Tyear = Tyear.strftime("%Y")
    result = zhishupinghua(start, end, Tyear = Tyear, premaxload = premaxload)
    tag = args["tag"]
    tagType = args["tagType"]
    content = {}
    content['arg'] = args
    content["result"] = result
    re = insertAlgorithmContent(tag, tagType, content)

    return content

def DailyTypicalOp(year,periodnum,category):
    beginyear = timeFormat(year, "year")
    endyear = getEndYear(beginyear)
    start = beginyear.strftime("%Y/%m/%d")
    end = endyear.strftime("%Y/%m/%d")
    result = typicalDay(start, end, periodnum)
    if category == "最大负荷":
        re = result[3].tolist()
    elif category == "最小负荷":
        re = result[4].tolist()
    elif category == "中位负荷":
        re = result[5].tolist()
    d_max, d_mean, d_min, d_r, d_m_r, peak, peak_r = d_pre_character(re)
    data = {
        'dayMaxPayload': d_max,
        'dayMinPayload': d_min,
        'dayAveragePayload': d_mean,
        'dayPayloadRate': d_r,
        'dayMinPayloadRate': d_m_r,
        'dayPeekValleyDiff': peak,
        'dayPeekValleyDiffRate': peak_r
    }
    content = {
        "data":data,
        "re": re
    }
    return content

def ChartMonthlyOp(year, category):
    beginyear = timeFormat(year, "year")
    endyear = getEndYear(beginyear)
    start = beginyear.strftime("%Y/%m/%d")
    end = endyear.strftime("%Y/%m/%d")
    if category == "年负荷曲线":
        return yearLoad(start, end)
    elif category == "年持续负荷曲线":
        return yearLoadCon(start,end)
    else:
        beginMonth = beginyear
        endMonth = getNextYear(beginyear)
        endMonth = endMonth - timedelta(days=1)
        # print(beginMonth)
        # print(endMonth)
        result1 = []
        result2 = []
        result3 = []
        result4 = []

        result = monthFeature(beginMonth.strftime('%Y/%m/%d'), endMonth.strftime('%Y/%m/%d'))
        # print(result)
        for temp in result:
            result1.append(temp["monthAverageDailyPayload"])
            result2.append(temp["monthAverageDailyPayloadRate"])
            result3.append(temp["monthMaxPeekValleyDiff"])
            result4.append(temp["monthMaxPeekValleyDiffRate"])

        # while beginMonth < endMonth:
        #     t = beginMonth.strftime('%Y/%m/%d')
        #     te = getEndMonth(beginMonth)
        #     te = te.strftime("%Y/%m/%d")
        #     temp = monthFeature(start=t, end=te)
        #     result1.append(temp["monthAverageDailyPayload"])
        #     result2.append(temp["monthAverageDailyPayloadRate"])
        #     result3.append(temp["monthMaxPeekValleyDiff"])
        #     result4.append(temp["monthMaxPeekValleyDiffRate"])
        #     beginMonth = getNextMonth(beginMonth)
        #     print(t)
        if category == "月平均日负荷曲线":
            return result1
        elif category == "月平均日负荷率曲线":
            return result2
        elif category == "月最大峰谷差曲线":
            return result3
        elif category == "月最大峰谷差率曲线":
            return result4

def payloadChartsDaily(day):

    result = dayLoad(day, day)

    return result
def payloadChartsYearly(args):
    beginyear = args["beginYear"]
    beginyear = timeFormat(beginyear, "year")
    endyear = args["endYear"]
    endyear = timeFormat(endyear, "year")
    endyear = getEndYear(endyear)
    start = beginyear.strftime("%Y/%m/%d")
    end = endyear.strftime("%Y/%m/%d")
    category = args["category"]
    # print(endyear)
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result = yearfeature(start, end)
    for temp in result:
        result1.append(temp["yearMaxPayload"])
        result2.append(temp["yearAverageDailyPayloadRate"])
        result3.append(temp["yearMaxPeekValleyDiff"])
        result4.append(temp["monthImbaRate"])
        result5.append(temp["seasonImbaRate"])

    if category == "历年最大负荷曲线":
        return result1
    elif category == "历年平均日负荷率曲线":
        return result2
    elif category == "历年最大峰谷差曲线":
        return result3
    elif category == "历年月不均衡曲线":
        return result4
    elif category == "历年季不平衡系数曲线":
        return result5

def industryMixModelValidate(methods):
    methodlist = []
    for i in methods:
        name = methodNameZhToEn(zh=i)
        methodlist.append(name)
    # 补充算法模型
    re = True
    return re



def regionMixModelValidate(methods):
    methodlist = []
    for i in methods:
        name = methodNameZhToEn(zh = i)
        methodlist.append(name)

    # 补充算法模型
    re = True
    return re

def miningResults(tagType):
    re = getTagByKind(tagType)
    return re

def regionQueryCon():
    re = getArea()
    return re

def industryQuery():
    re = getKind()
    return re

def grainQuery():
    re = getGrain()

    return re

def getDatas(location, dataName, startTime, endTime):
    re = getData(location, dataName, startTime, endTime)
    return re
def executeAlgorithmTest(method, args):
    executeAlgorithm(method, args)


def getDefault(start, end):
    file = "yunnan_year_loadchara-fengshui-souku-max"
    result = {}
    loadmax, electricity = default_jiabi(file, start, end)

    result["jiabi"] = {
        "maxPayload": loadmax,
        "dailyAmount": electricity
    }
    loadmax, electricity = default_f(file, start, end)
    result["fenxing"] = {
        "maxPayload": loadmax,
        "dailyAmount": electricity
    }
    load_max, electricity, gamma, beta = default_souku(file, start, end)
    result["souku"] = {
        "maxPayload": loadmax,
        "dailyAmount": electricity,
        "gamma":gamma,
        "beta":beta
    }
    return result

def getMetaDataTree():
    result = []
    mtd = getMetaData()
    saved1 = []
    tichu = ['保山','楚雄','大理', '德宏', '迪庆', '红河', '昆明','丽江','临沧', '怒江', '普洱', '曲靖', '文山', '西双版纳', '玉溪', '昭通', 'yunnan']
    for i in mtd:
        # print(i)
        if i[1] in tichu:
            continue
        for y in saved1:
            if y[1] == i[1] and y[2] == i[2]:
                continue
        saved1.append((i[1], i[2]))
        re = getDataNameByAreaAndKind(i[1], i[2])
        if len(re) == 0:
            continue
        tmp = {"value": i[2], "label": i[2], "children": []}
        for d in re:
            temp = {"label": d, "value": d}
            tmp["children"].append(temp)
        result.append(tmp)
    print(saved1)
    return result

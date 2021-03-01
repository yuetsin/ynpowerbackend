# from dao.interface import getDataByCondition, modifyDataByCondition, getTagByKind, getAllTag, renameTag, deleteTag, \
#     checkTag, insertAlgorithmContent, getGrain, getKind, getArea
from dao import *
from utils import *


def exceptQuery(category, startTime, endTime, grain, area):
    data = getDataByCondition(grain = grain, startTime = startTime, endTime = endTime, kind = category[0], dataName = category[1], area = area)
    datalist = []
    if data is not None:
        for d in data:
            temp = {}
            temp["key"] = d[0]
            temp["category"] = [d[5], d[1]]
            temp['region'] = d[4]
            temp['grain'] = d[3]
            temp['value'] = d[2]
            temp["suggest"] = -1
            datalist.append(temp)
    else:
        return None
    # f = getAlgorithm("Outlier")

    result = datalist #异常数据检测算法
    return result

def exceptResolve(originData, modifiedData):
    re = modifyDataByCondition(modifiedData['value'], grain =originData['grain'], startTime = originData['key'], endTime = originData['key'], kind = originData['category'][0], dataName = originData['category'][1], area = originData['region'])
    return re

def exceptAccept(acceptData):
    re = modifyDataByCondition(acceptData['value'], grain=acceptData['grain'], startTime=acceptData['key'],
                               endTime=acceptData['key'], kind=acceptData['category'][0],
                               dataName=acceptData['category'][1], area=acceptData['region'])
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
    data = getDataByCondition(grain=None, startTime=str(beginYear), endTime=str(endYear), kind=None, dataName=None,
                              area=region)  # 是否需要粒度，和kind，dataname
    f = getAlgorithm(method)
    result = None
    if method == "Pearson":
        threshold = arg['threshold']
        result = f()
    elif method == "KMeans":
        suggestCategoryCount = arg['suggestCategoryCount']
        categoryCount = arg['categoryCount']
        result = f()
    elif method == "PCA":
        absThreshold = arg['absThreshold']
        result = f()
    elif method == "ARL":
        minSupport = arg['minSupport']
        minConfidence = arg['minConfidence']
        result = f()
    # (tag, tagType, region, factors, method, pearson, beginYear, endYear)

    content = {}
    content['arg'] = args
    content['result'] = result
    #补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return re


def regionSinglePredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    historyBeginYear = args['historyBeginYear']
    historyEndYear = args['historyEndYear']
    factor1= args['factor1']
    name1 = factor1['name']
    hasValue1 = factor1['hasValue']
    value1 = factor1['value']

    factor2= args['factor2']
    name = factor2['name']
    hasValue= factor2['hasValue']
    value= factor2['value']
    data = getDataByCondition(grain=None, startTime=str(beginYear), endTime=str(endYear), kind=industry, dataName=None,
                              area=region)  # 是否需要粒度，和kind，dataname
    result = executeAlgorithm(method)


    content = {}
    content['arg'] = args
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return re

def regionMixPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    historyBeginYear = args['historyBeginYear']
    historyEndYear = args['historyEndYear']
    selectedMethods = args['selectedMethods']
    data = getDataByCondition(grain=None, startTime=str(beginYear), endTime=str(endYear), kind=industry, dataName=None,
                              area=region)  # 是否需要粒度，和kind，dataname
    content = {}
    content['arg'] = args
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return re


def industrySinglePredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    historyBeginYear = args['historyBeginYear']
    historyEndYear = args['historyEndYear']
    method = args['method']
    parameters = args['parameters']
    data = getDataByCondition(grain=None, startTime=str(beginYear), endTime=str(endYear), kind=industry, dataName=None,
                              area=region)  # 是否需要粒度，和kind，dataname
    content = {}
    content['arg'] = args
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return re

def industryMixPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    historyBeginYear = args['historyBeginYear']
    historyEndYear = args['historyEndYear']
    selectedMethods = args['selectedMethods']
    data = getDataByCondition(grain=None, startTime=str(beginYear), endTime=str(endYear), kind=industry, dataName=None,
                              area=region)  # 是否需要粒度，和kind，dataname
    content = {}
    content['arg'] = args
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return re

def saturationCurvePredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    historyBeginYear = args['historyBeginYear']
    historyEndYear = args['historyEndYear']
    method = args['method']
    data = getDataByCondition(grain=None, startTime=str(beginYear), endTime=str(endYear), kind=industry, dataName=None,
                              area=region)  # 是否需要粒度，和kind，dataname
    content = {}
    content['arg'] = args
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return re

def payloadDensityPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    historyBeginYear = args['historyBeginYear']
    historyEndYear = args['historyEndYear']
    method = args['method']
    data = getDataByCondition(grain=None, startTime=str(beginYear), endTime=str(endYear), kind=industry, dataName=None,
                              area=region)  # 是否需要粒度，和kind，dataname
    content = {}
    content['arg'] = args
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return re


def provincialAndMunicipalPredict(args):
    historyBeginYear = args['historyBeginYear']
    historyEndYear = args['historyEndYear']
    predictYear = args['predictYear']
    provPlan = args['provPlan'] # 如果设置为 `__byUpload__` 则从上传文件中读取
    provFile = args['provFile']  # 如果 provPlan 是 __byUpload__，那么从这里读
    muniData  = args['muniData']
    # 补充算法模型
    re = {}
    return re

def bigDataPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    historyBeginYear = args['historyBeginYear']
    historyEndYear = args['historyEndYear']
    method = args['method']
    patches = args['patches']
    data = getDataByCondition(grain=None, startTime=str(beginYear), endTime=str(endYear), kind=industry, dataName=None,
                              area=region)  # 是否需要粒度，和kind，dataname
    content = {}
    content['arg'] = args
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return re

def dailyPayloadTraits(args):
    beginDay = args['beginDay']
    endDay = args['endDay']

    data = getDataByCondition(grain="day", startTime=beginDay, endTime=endDay, kind=None, dataName=None,
                              area=None)
    content = {}
    content['arg'] = args
    content['content'] = []
    # 补充算法模型
    # re = insertAlgorithmContent(tag, tagType, content)
    return content
def monthlyPayloadTraits(args):
    beginMonth = args['beginMonth']
    endMonth = args['endMonth']
    data = getDataByCondition(grain="month", startTime=beginMonth, endTime=endMonth, kind=None, dataName=None,
                              area=None)
    content = {}
    content['arg'] = args
    content['content'] = []
    # 补充算法模型
    # re = insertAlgorithmContent(tag, tagType, content)
    return content

def yearlyPayloadTraits(args):
    beginYear = args['beginYear']
    endYear = args['endYear']
    data = getDataByCondition(grain="year", startTime=beginYear, endTime=endYear, kind=None, dataName=None,
                              area=None)
    content = {}
    content['arg'] = args
    content["content"] = []
    # 补充算法模型
    # re = insertAlgorithmContent(tag, tagType, content)
    return content


def sokuPayloadPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    startYear = args['beginYear']
    endYear = args['endYear']
    season = args["season"]  # 2 or 3 or 4, Spring, Summer, Autumn, Winter
    predictMaxPayload= args["maxPayload"]
    predictDailyAmount= args["dailyAmount"]
    gammaValue= args["gamma"]
    betaValue= args["beta"]
    data = getDataByCondition(grain=None, startTime=str(startYear), endTime=str(endYear), kind=None, dataName=None,
                              area=None)
    content = {}
    content['arg'] = args
    content['content'] =[]
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return content


def clampingPayloadPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    startYear = args['beginYear']
    endYear = args['endYear']
    season = args["season"]  # 2 or 3 or 4, Spring, Summer, Autumn, Winter
    predictMaxPayload= args["maxPayload"]
    predictDailyAmount= args["dailyAmount"]

    data = getDataByCondition(grain=None, startTime=str(startYear), endTime=str(endYear), kind=None, dataName=None,
                              area=None)
    method = args["name"]
    result = executeAlgorithm(method, args)
    content = {}
    content['arg'] = args
    content['content'] = []
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return content


def interpolatingPayloadPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    startYear = args['beginYear']
    endYear = args['endYear']
    season = args["season"]  # 2 or 3 or 4, Spring, Summer, Autumn, Winter
    predictMaxPayload = args["maxPayload"]
    predictDailyAmount = args["dailyAmount"]

    data = getDataByCondition(grain=None, startTime=str(startYear), endTime=str(endYear), kind=None, dataName=None,
                              area=None)
    content = {}
    content['arg'] = args
    content['content'] = []
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return content

def yearlyContinuousPayloadPredict(args):
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    startYear = args['beginYear']
    endYear = args['endYear']
    predictMaxPayload = args["maxPayload"]
    data = getDataByCondition(grain=None, startTime=str(startYear), endTime=str(endYear), kind=None, dataName=None,
                              area=None)
    content = {}
    content['arg'] = args
    content['content']  = []
    # 补充算法模型
    re = insertAlgorithmContent(tag, tagType, content)
    return content


def payloadChartsDaily(day):
    re = {}
    return re

def payloadChartsYearly(beginYear, endYear, category):
    re = {}
    return re


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
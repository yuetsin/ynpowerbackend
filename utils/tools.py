from datetime import datetime, timedelta
import re
from dateutil.relativedelta import relativedelta
# import matlab.engine
import pandas as pd
#
# eng = matlab.engine.start_matlab()

# zhlist = ['基于ARIMA季节分解的行业电量预测', '基于EEMD的行业用电量预测', '基于主成分因子的行业用电量预测', '基于随机森林的行业用电量预测', '基于神经网络的行业用电量预测', '灰色滑动平均模型', '基于滚动机制的灰色预测模型', '模糊线性回归模型', '模糊指数平滑模型', '组合预测模型', '梯度提升模型', '支持向量机模型', 'BP神经网络模型', '循环神经网络模型', '长短期神经网络模型', '扩展索洛模型', '分位数回归模型', '一元线性函数', '生长函数', '指数函数', '对数函数', '二元一次函数', '一元线性外推', '生长函数外推', '指数函数外推', '对数函数外推', '饱和曲线法', '负荷密度法', '大用户法', '增长率法', '数据异常检测', 'K均值算法', '主成分分析算法', '关联规则分析算法']
# english = ['SARIMAIndustry', 'EEMDIndustry', 'PCAIndustry', 'RFIndustry', 'BPNNIndustry', 'GM', 'GPRM', 'FLR', 'FER',
#      'Combination', 'GBDT', 'SVM', 'BPNN', 'RNN', 'LSTM', 'ESQRM', 'QuantileRegression', 'Unarylinear', 'Growth',
#      'Exponent', 'Logarithm', 'Binarylinear', 'UnarylinearTime', 'GrowthTime', 'ExponentTime', 'LogarithmTime',
#      'SaturationCurve', 'LDM', 'ForIndustry', 'Increase', 'Outlier', 'Kmeans', 'PCA', 'AssociationRule']

#flag = 0,开始时间，flag=1，结束时间


def formateTimeString(t, grain, flag):
    timestr = ""
    timet = None
    tlist = re.split('/|:| ', t)
    # print(tlist)
    n = len(tlist)
    if n == 1:
        timet = datetime.strptime(t, '%Y')
    elif n == 2:
        timet = datetime.strptime(t, '%Y/%m')
    elif n == 3:
        timet = datetime.strptime(t, '%Y/%m/%d')
    elif n == 4:
        timet = datetime.strptime(t, '%Y/%m/%d %H')
    elif n == 5:
        timet = datetime.strptime(t, '%Y/%m/%d %H:%M')
    elif n == 6:
        timet = datetime.strptime(t, '%Y/%m/%d %H:%M:%S')
    if flag == 0:
        timestr = timet.strftime('%Y-%m-%d %H:%M:%S')
    elif flag == 1:
        if grain == 'day':
            timet = timet + timedelta(days=1) - timedelta(seconds=1)
            timestr = timet.strftime('%Y-%m-%d %H:%M:%S')
        elif grain == 'month':
            timet = timet + relativedelta(months=1) - timedelta(seconds=1)
            timestr = timet.strftime('%Y-%m-%d %H:%M:%S')
        elif grain == 'hour':
            timet = timet + timedelta(hours=1) - timedelta(seconds=1)
            timestr = timet.strftime('%Y-%m-%d %H:%M:%S')
        elif grain == 'min':
            timet = timet + timedelta(minutes=1) - timedelta(seconds=1)
            timestr = timet.strftime('%Y-%m-%d %H:%M:%S')
        elif grain == 'sec':
            timestr = timet.strftime('%Y-%m-%d %H:%M:%S')
        else:
            timet = timet + relativedelta(years=1) - timedelta(seconds=1)
            timestr = timet.strftime('%Y-%m-%d %H:%M:%S')
    # print(timestr)
    return timestr

def formatMetadataCondition(grain = None, kind = None, area = None):
    whe = []
    if area is not None:
        whe.append("area = '{}'".format(area))
    if kind is not None:
        whe.append("kind = '{}'".format(kind))

    if grain is not None:
        whe.append("grain = '{}'".format(grain))

    return whe

#组合数据的查询或者修改条件
def formatDataCondition(startTime = None, endTime = None, dataName = None, grain = None, metadataIds = None):
    whe = []
    # print(startTime)
    if grain == None:
        startTime = formateTimeString(startTime, "sec", 0)
        endTime = formateTimeString(endTime, "sec", 1)
    else:
        startTime = formateTimeString(startTime, grain, 0)
        endTime = formateTimeString(endTime, grain, 1)
    if grain != None:
        whe.append("grain = '{}'".format(grain))

    if dataName != None:
        dataNamelist = dataName.split(',')
        dataNames = ""
        for i in range(len(dataNamelist)):
            dataNames += "'" + dataNamelist[i] + "'"
            if i != len(dataNamelist) - 1:
                dataNames += ","
        whe.append("dataName in ({})".format(dataNames))

    if startTime != None:
        whe.append("datatime >= '{}'".format(startTime))
    if endTime != None:
        whe.append("datatime <= '{}'".format(endTime))
    if metadataIds != None:
        whe.append("metadataid in ({})".format(",".join(metadataIds)))
    # print(whe)
    return whe

def timeFormat(t, grain):
    if grain == "year":
        timet = datetime.strptime(t, '%Y')
    elif grain == "month":
        timet = datetime.strptime(t, '%Y/%m')
    elif grain == "day":
        timet = datetime.strptime(t, '%Y/%m/%d')
    return timet

#获取后一天
def getNextDay(t):
    timet = t + timedelta(days=1)
    return timet
def getEndYear(t):
    timet = t + relativedelta(years=1) - timedelta(days=1)
    return timet
def getNextYear(t):
    timet = t + relativedelta(years=1)
    return timet

def getEndMonth(t):
    timet = t + relativedelta(months=1) - timedelta(days=1)
    return timet
def getNextMonth(t):
    timet = t + relativedelta(months=1)
    return timet

#解析一些相同的参数
def getArgs(args):
    try:
        beginYear = args['beginYear']
    except:
        beginYear = None
    try:
        endYear = args['endYear']
    except:
        endYear = None
    try:
        region = args['region']
    except:
        region = None
    try:
        industry = args['industry']
    except:
        industry = None
    try:
        method = args['method']
    except:
        method = None
    try:
        tag = args['tag'],
        if type(tag) is not str:
            tag = tag[0]
    except:
        tag = None
    try:
        tagType = args['tagType']
    except:
        tagType = None
    return beginYear, endYear, region, industry, method, tag, tagType

def methodNameZhToEn( zhlist, english, zh = None, en = None):

    if en is None and zh is None:
        return None
    # elif en is not None:
    #     for i in range(len(english)):
    #         if english[i] == en:
    #             return zhlist[i]
    elif en is not None:
        return en
    elif zh is not None:
        for i in range(len(zhlist)):
            if zhlist[i] == zh:
                return english[i]


def getAlgorithmName(filename):
    data = pd.read_excel(filename, None, index_col=None)
    zhname = []
    enname = []
    for row in data.values():
        x, y = row.shape
        header = [i for i in row.columns]
        for j in range(1, y):
            enname.append(header[j])
            zhname.append(row.iloc[0][j])
    return zhname, enname


def getAlgorithm(name):
    dd = __import__("algorithms." + name, fromlist = True)
    f = getattr(dd, name)
    # print(f)
    return f

def formatPredictResult(result):
    tableTwoData = []
    prefromyear = timeFormat(result["prefromyear"], "year")
    pretoyear = timeFormat(result["pretoyear"], "year")
    i = 0
    while prefromyear <= pretoyear:
        temp={
            'year': prefromyear.strftime("%Y"),
            'predict': result['preresult'][i]
        }
        tableTwoData.append(temp)
        i += 1
        prefromyear = getNextYear(prefromyear)

    re ={
        "tableOneData":[
            {
            'mape': result["MAPE"],
            "rmse": result["RMSE"]
            }
        ],
        "tableTwoData": tableTwoData
    }
    return re


def executeAlgorithmtest(method, args):

    # arg = getAlgorithmArgs(method, filename)
    a, b = getAlgorithmName(filename)
    method = methodNameZhToEn(a, b, method)

    f = getAlgorithm(method)
    # print(arg)
    argstr = ""
    for v in args:
        if v == "method":
            continue
        if v[-1] == "*":
            k = v[:-1]
        else:
            k = v
        if type(args[v]) == int:
            argstr += "{} = {},".format(k, args[v])
        else:
            argstr += "{} = '{}',".format(k, args[v])

    print(argstr)
    result = eval("f("+argstr+")")
    return result
    beginYear, endYear, region, industry, method, tag, tagType = getArgs(args)
    if method == "SVM":
        for v in args:
            if v == "method":
                continue
            exec('var{} = {}'.format(v, args[v]))
        # historyBeginYear = args['historyBeginYear']
        # historyEndYear = args['historyEndYear']
        # factor1 = args['factor1']
        # name1 = factor1['name']
        # hasValue1 = factor1['hasValue']
        # value1 = factor1['value']
        #
        # factor2 = args['factor2']
        # name = factor2['name']
        # hasValue = factor2['hasValue']
        # value = factor2['value']
        # presult = f(StartYear, EndYear, PreStartYear, PreEndYear, timestep, pretype, city)

        # presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=10, pretype="consumption", city = region)
        # return presult
    elif method == "PCAIndustry":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype= None, econamelist= None, city = None)
        return presult
    elif method == "RFIndustry":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None, n_estimators = None, city=None)
        return presult
    elif method == "BPNNIndustry":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    city=None, hidden=None, learningrate = None, epoch = None)
        return presult
    elif method == "GM":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    city=None)
        return presult
    elif method == "GPRM":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    city=None)
        return presult
    elif method == "FLR":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    city=None)
        return presult
    elif method == "FER":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    city=None)
        return presult
    elif method == "Combination":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(beginYear, endYear, pretype=None, singleresult=None,
                    city=None, comtype=None)
        return presult
    elif method == "GBDT":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    city=None,LearningRate = None, Maxdepth=None, NumberofEstimators=None)
        return presult
    elif method == "RandomForest":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    n_estimators=None, city=None)
        return presult
    elif method == "BPNN":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    city=None, hidden=None, learningrate=None, epoch=None)
        return presult
    elif method == "RNNpre":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    city=None, hidden_size=None, hidden_layer=None, learningrate=None, epoch=None)
        return presult
    elif method == "LSTMpre":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, timestep=None, pretype=None,
                    city=None, hidden_size=None, hidden_layer=None, learningrate=None, epoch=None)
        return presult
    elif method == "ESQRM":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, quatile=None, pretype=None, econamelist=None, city=None)
        return presult

    elif method == "QuantileRegression":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, quatile=None, pretype=None, econamelist=None,
                    city=None)
        return presult
    elif method == "Unarylinear":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype=None, econamelist=None,
                    city=None, planflag=None, plan=None)
        return presult
    elif method == "Growth":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype=None, econamelist=None,
                    city=None, planflag=None, plan=None)
        return presult
    elif method == "Exponent":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype=None, econamelist=None,
                    city=None, planflag=None, plan=None)
        return presult
    elif method == "Logarithm":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype=None, econamelist=None,
                    city=None, planflag=None, plan=None)
        return presult
    elif method == "Binarylinear":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype=None, econamelist=None,
                    city=None, planflag1=None, plan1=None, planflag2=None, plan2=None)
        return presult
    elif method == "UnarylinearTime":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype=None,
                    city=None, planflag=None, plan=None)
        return presult
    elif method == "GrowthTime":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype=None,
                    city=None, planflag=None, plan=None)
        return presult
    elif method == "ExponentTime":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype=None,
                    city=None, planflag=None, plan=None)
        return presult
    elif method == "LogarithmTime":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, pretype=None,
                    city=None, planflag=None, plan=None)
        return presult
    elif method == "SaturationCurve":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, feature=None, pretype=None,
                    city=None)
        return presult
    elif method == "LDM":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, building=None, density = None, pretype=None,
                    city=None)
        return presult
    elif method == "ForIndustry":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, rejectlsit=None, proposedata=None, pretype=None,
                    city=None)
        return presult
    elif method == "Increase":
        historyBeginYear = args['historyBeginYear']
        historyEndYear = args['historyEndYear']
        presult = f(historyBeginYear, historyEndYear, beginYear, endYear, rate=None, pretype=None,
                    city=None)
        return presult
    elif method == "Outlier":
        presult = f(beginYear, endYear,pretype=None, city=None)
        return presult
    elif method == "CoordinationCityandProvince":
        presult = f(beginYear, endYear, cityname=None, cityrealdata=None, citypredata = None, provincerealdata= None, provincepredata=None,pretype = None, province=None)
        return presult
    elif method == "Kmeans":
        presult = f(beginYear, endYear, VariablesName=None, EndStartYear=None)
        return presult
    elif method == "PCA":
        presult = f(beginYear, endYear, VariablesName=None, EndStartYear=None)
        return presult
    elif method == "AssociationRule":
        presult = f(beginYear, endYear, VariablesName=None, EndStartYear=None, MinConf = None)
        return presult
    elif method == "SARIMAIndustry":
        presult = f(StartYear=None, EndYear=None, PreStartYear=None, EndStartYear=None,)
        return presult
    elif method == "EEMDIndustry":
        presult = f(StartYear=None, EndYear=None, PreStartYear=None, EndStartYear=None,)
        return presult


if __name__ == '__main__':
    getAlgorithm("GM")
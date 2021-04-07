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

#获取loadpredict的file参数
def getFilenameOfLoadPre(season, type, func):
    if season == "丰水期" and type == "最大值" and func == "fx":
        return "yunnan_year_fengshui_f_max"
    elif season == "丰水期" and type == "最小值" and func == "fx":
        return "yunnan_year_fengshui_f_min"
    elif season == "丰水期" and type == "中位值" and func == "fx":
        return "yunnan_year_fengshui_f_median"
    elif season == "丰水期" and type == "最大值" and func == "jb":
        return "yunnan_year_fengshui_jiabi_max"
    elif season == "丰水期" and type == "最小值" and func == "jb":
        return "yunnan_year_fengshui_jiabi_min"
    elif season == "丰水期" and type == "中位值" and func == "jb":
        return "yunnan_year_fengshui_jiabi_median"
    elif season == "丰水期" and type == "最大值" and func == "sk":
        return "yunnan_year_fengshui_souku_max"
    elif season == "丰水期" and type == "最小值" and func == "sk":
        return "yunnan_year_fengshui_souku_min"
    elif season == "丰水期" and type == "中位值" and func == "sk":
        return "yunnan_year_fengshui_souku_median"
    elif season == "汛后枯期" and type == "最大值" and func == "fx":
        return "yunnan_year_xunhou_f_max"
    elif season == "汛后枯期" and type == "最小值" and func == "fx":
        return "yunnan_year_xunhou_f_min"
    elif season == "汛后枯期" and type == "中位值" and func == "fx":
        return "yunnan_year_xunhou_f_median"
    elif season == "汛后枯期" and type == "最大值" and func == "jb":
        return "yunnan_year_xunhou_jiabi_max"
    elif season == "汛后枯期" and type == "最小值" and func == "jb":
        return "yunnan_year_xunhou_jiabi_min"
    elif season == "汛后枯期" and type == "中位值" and func == "jb":
        return "yunnan_year_xunhou_jiabi_median"
    elif season == "汛后枯期" and type == "最大值" and func == "sk":
        return "yunnan_year_xunhou_souku_max"
    elif season == "汛后枯期" and type == "最小值" and func == "sk":
        return "yunnan_year_xunhou_souku_min"
    elif season == "汛后枯期" and type == "中位值" and func == "sk":
        return "yunnan_year_xunhou_souku_median"
    elif season == "汛前枯期" and type == "最大值" and func == "fx":
        return "yunnan_year_xunqian_f_max"
    elif season == "汛前枯期" and type == "最小值" and func == "fx":
        return "yunnan_year_xunqian_f_min"
    elif season == "汛前枯期" and type == "中位值" and func == "fx":
        return "yunnan_year_xunqian_f_median"
    elif season == "汛前枯期" and type == "最大值" and func == "jb":
        return "yunnan_year_xunqian_jiabi_max"
    elif season == "汛前枯期" and type == "最小值" and func == "jb":
        return "yunnan_year_xunqian_jiabi_min"
    elif season == "汛前枯期" and type == "中位值" and func == "jb":
        return "yunnan_year_xunqian_jiabi_median"
    elif season == "汛前枯期" and type == "最大值" and func == "sk":
        return "yunnan_year_xunqian_souku_max"
    elif season == "汛前枯期" and type == "最小值" and func == "sk":
        return "yunnan_year_xunqian_souku_min"
    elif season == "汛前枯期" and type == "中位值" and func == "sk":
        return "yunnan_year_xunqian_souku_median"


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


def getAlgorithmName(filename, kind = None):
    if kind == None:
        data = pd.read_excel(filename, None, index_col=None)
    else:
        data = pd.read_excel(filename, index_col=None, sheet_name=kind)
    zhname = []
    enname = []
    if type(data) is dict:

        for row in data.values():
            # print(row)
            x, y = row.shape
            header = [i for i in row.columns]
            for j in range(1, y):
                enname.append(header[j])
                zhname.append(row.iloc[0][j])
    else:
        # print(data)
        x, y = data.shape
        header = [i for i in data.columns]
        for j in range(1, y):
            enname.append(header[j])
            zhname.append(data.iloc[0][j])
    return zhname, enname

def getAlgorithm(name):
    dd = __import__("algorithms." + name, fromlist= True)
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
            'predict': round(result['preresult'][i],2)
        }
        tableTwoData.append(temp)
        i += 1
        prefromyear = getNextYear(prefromyear)

    re ={
        "tableOneData":[
            {
            'mape': round(result["MAPE"],2),
            "rmse": round(result["RMSE"],2)
            }
        ],
        "tableTwoData": tableTwoData
    }
    return re

def getCombinationMethod():
    return ["等权组合", "加权组合", "递阶组合"]


if __name__ == '__main__':
    getAlgorithm("GM")
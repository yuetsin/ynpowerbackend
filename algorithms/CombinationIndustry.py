# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:10:55 2021

@author: ZR_YL
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import copy
from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json 





def CombinationIndustry(PreStartYear,PreEndYear,pretype,singleresult,city="云南省", comtype="等权组合"):

    """
    

    Parameters
    ----------
    PreStartYear : TYPE
        DESCRIPTION.
    PreEndYear : TYPE
        DESCRIPTION.
    pretype : TYPE
        DESCRIPTION.
    singleresult : list
        单预测模型的结果,list形式,每个元素为dict.
    city_or_industry : TYPE, optional
        DESCRIPTION. The default is "云南省".
    comtype : TYPE, optional
        选择组合方法，有"等权组合","加权组合" 和 "递阶组合"可选. The default is "等权组合".

    Returns
    -------
    None.

    """


    number=len(singleresult)
    def findtrain(singleresult,n):
        
        start="0"
        end="29999999"
        for i in range(n):
            startyear=singleresult[i].get("trainfromyear")
            endyear=singleresult[i].get("traintoyear")
            if int(startyear)> int(start):
                start=startyear
            if int(endyear) < int(end):
                end=endyear
        if int(end)-int(start)<0:
            return None, None
        else:
            return start, end
    
    def normalization(index):
        #根据评价指标权重
        indexsum=sum(index)
        weight=[]
        for i in range(len(index)):
            w=1-index[i]/indexsum
            weight.append(w)
        
        weightsum=sum(weight)
        finalweight=[x/weightsum for x in weight]
        return finalweight
    
    trainyear=[0,0]
    trainyear[0], trainyear[1] = findtrain(singleresult,number)
    #构建训练数据集，numpy格式,同时获取预测数据集，numpy格式
    if trainyear[0] != None:
        traindata=[]
        predata = []
        singlermse = []
        singlemape = []
        for i in range(number):
            StartYear=singleresult[i].get("trainfromyear")
            EndYear=singleresult[i].get("traintoyear")
            realyear = np.arange(int(StartYear),int(EndYear)+1)
            
            a=np.where(realyear == int(trainyear[0]))[0][0]
            b=np.where(realyear == int(trainyear[1]))[0][0]
            tdata=singleresult[i].get("trainresult")[a:b+1]
            pdata=singleresult[i].get("preresult")
            traindata.append(tdata)
            predata.append(pdata)
            singlermse.append(singleresult[i].get("RMSE"))
            singlemape.append(singleresult[i].get("MAPE"))
    
    traindata=np.array(traindata)
    predata=np.array(predata)
    
    #获取训练数据对应的真实数据
    datajson=getData("云南省_year_电力电量类-行业", pretype, trainyear[0], trainyear[1])
    data=json.loads(datajson)     
    realtraindata=[]
    for i in data.values():
        realtraindata.append(i) 
    realtraindata=np.array(realtraindata)
    
    if comtype == "等权组合":
        
        meancombination=predata.mean(axis=0)
        trainmeancombination=traindata.mean(axis=0)
        rmse=RMSE(trainmeancombination,realtraindata)
        mape=MAPE(trainmeancombination,realtraindata)
        ytrain=trainmeancombination.tolist()
        ypre=meancombination.tolist()
    
    elif comtype == "加权组合":
        weight=normalization(singlermse)
        weightcombination=np.average(predata,weights=weight,axis=0)
        trainweightcombination=np.average(traindata,weights=weight,axis=0)
        rmse=RMSE(trainweightcombination,realtraindata)
        mape=MAPE(trainweightcombination,realtraindata)  

        ytrain=trainweightcombination.tolist()
        ypre=weightcombination.tolist()
    elif comtype == "递阶组合":
        againdata=copy.deepcopy(predata)
        againtrain=copy.deepcopy(traindata)
        for k in range(10):
            weight=normalization(singlermse)
            # print(weight)
            reweightcombination=np.average(againdata,weights=weight,axis=0)    
            
            retrainweightcombination=np.average(againtrain,weights=weight,axis=0)
            r=RMSE(retrainweightcombination,realtraindata)
            
            if min(weight)>1/(len(predata)+1):
                break
            #比较权重，进行数据代替
            dex=0
            replace=0
            for w in range(len(singlermse)):
                if singlermse[w]>r:
                    if singlermse[w]>replace:
                        dex=w
                        replace=singlermse[w]
            
            singlermse[dex]=r
            againdata[dex]=reweightcombination
            againtrain[dex]=retrainweightcombination
            
        rmse=RMSE(retrainweightcombination,realtraindata)
        mape=MAPE(retrainweightcombination,realtraindata)  

        ytrain=retrainweightcombination.tolist()
        ypre=reweightcombination.tolist()        
    
    
    result = {"trainfromyear":trainyear[0],"traintoyear":trainyear[1],"trainresult":ytrain,"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre,"MAPE":mape,"RMSE":rmse}
    return result

if __name__ == '__main__':
    StartYear = "1990"
    EndYear = "2019"
    PreStartYear = "2020"
    PreEndYear = "2029"
    timestep = 15
    pretype = "第一产业用电量"
    comtype="递阶组合"
    city="云南省"
    #
    # #运行单预测模型
    # resultGBDT=GBDT.GBDT(StartYear,EndYear,PreStartYear,PreEndYear,timestep)
    # resultExponentTime=ExponentTime.ExponentTime(StartYear,EndYear,PreStartYear,PreEndYear)
    # resultBPNN=BPNN.BPNN(StartYear,EndYear,PreStartYear,PreEndYear,timestep)
    #
    # content = {}
    # content['singlepre'] = resultGBDT, resultExponentTime, resultBPNN
    # r = ri.insertAlgorithmResult("combination", content)
    # #运行单预测模型部分在实际运行中不需要，直接从数据库中读取已有信息
    # r1 = ri.getAlgorithmResult("combination")
    # re = json.loads(r1)
    #
    # singleresult=json.loads(re.get("results")[0][1]).get('singlepre')
    # cresult=Combination(PreStartYear,PreEndYear,pretype,singleresult,comtype)
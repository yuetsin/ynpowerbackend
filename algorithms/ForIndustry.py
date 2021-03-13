# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 11:16:09 2021

@author: ZR_YL
"""


from evaluation import RMSE,MAPE
from dao.interface import getData, insertData
import json 
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
import math

import algorithms.ExponentTime
import algorithms.GrowthTime
import algorithms.UnarylinearTime
import algorithms.LogarithmTime
import algorithms.GM
import algorithms.GPRM
import algorithms.GBDT
import algorithms.RandomForest
import algorithms.SVM
import algorithms.FER
import algorithms.FLR

def ForIndustry(StartYear,EndYear,PreStartYear,PreEndYear,rejectlsit,proposedata,Premethod):

    pretype="consumption"
    propose = pd.read_csv(proposedata, encoding="UTF-8")
    
    if len(propose.values) != int(PreEndYear)-int(PreStartYear)+1:
        return {"prefromyear":None,"pretoyear":None,"preresult":"上传数据的年限与预测年限不符，请重新上传."}
    
    else:
        #读取年度数据
        name=[pretype]
        finaldata=[]
        yeardatajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
        yeardata=json.loads(yeardatajson)
        finaldata.append(yeardata)
        
        #读取行业数据
        for i in range(len(rejectlsit)):
            
            inddatajson=getData("yunnan_year_电力电量类", rejectlsit[i], StartYear, EndYear)
            inddata=json.loads(inddatajson)
            finaldata.append(inddata)
            name.append(rejectlsit[i])
            
        #获取最终数据DataFrame
        final=pd.DataFrame(finaldata,index=name)
        final=final.T
        final[pretype]=final[pretype].values*10000
        
        year=final.index.tolist()
        forpredata=[]
        for i in range(len(final)):
            drop=final[pretype].values[i]
            for j in range(len(rejectlsit)):
                drop=drop-final[rejectlsit[j]].values[i]
            forpredata.append(drop)
        
        
        savetype="剔除大用户的社会用电量"
        savetourl=pd.DataFrame()
        savetourl["year"]=year
        savetourl[savetype]=forpredata
        r=insertData(savetourl, "year","yunnan", "电力电量类")
        
        
        if Premethod=="指数函数外推":
            result= algorithms.ExponentTime(StartYear, EndYear, PreStartYear, PreEndYear, pretype = savetype, city="云南省")
        elif Premethod=="灰色滑动平均模型":
            T=math.floor(len(forpredata)/3)
            result= algorithms.GM(StartYear, EndYear, PreStartYear, PreEndYear, timestep=T, pretype=savetype, city="云南省")
        elif Premethod== "生长函数外推":
            result=algorithms.GrowthTime(StartYear, EndYear, PreStartYear, PreEndYear, pretype=savetype, city="云南省")
        elif Premethod== "一元线性外推":
            result= algorithms.UnarylinearTime(StartYear, EndYear, PreStartYear, PreEndYear, pretype=savetype, city="云南省")
        elif Premethod== "对数函数外推":
            result= algorithms.LogarithmTime(StartYear, EndYear, PreStartYear, PreEndYear, pretype=savetype, city="云南省")
        elif Premethod=="基于滚动机制的灰色预测模型":
            T=math.floor(len(forpredata)/3)
            result= algorithms.GPRM(StartYear, EndYear, PreStartYear, PreEndYear, T, pretype=savetype, city="云南省")
        elif Premethod== "模糊指数平滑模型":
            T=math.floor(len(forpredata)/3)
            result= algorithms.FER(StartYear, EndYear, PreStartYear, PreEndYear, T, pretype=savetype, city="云南省")
        elif Premethod=="模糊线性回归模型":
            T=math.floor(len(forpredata)/3)
            result= algorithms.FLR(StartYear, EndYear, PreStartYear, PreEndYear, T, pretype=savetype, city="云南省")
        elif Premethod == "梯度提升模型":
            T=math.floor(len(forpredata)/3)
            result= algorithms.GBDT(StartYear, EndYear, PreStartYear, PreEndYear, T, pretype=savetype, city="云南省")
        elif Premethod == "支持向量机模型":
            T=math.floor(len(forpredata)/3)
            result= algorithms.SVM(StartYear, EndYear, PreStartYear, PreEndYear, T, pretype=savetype, city="云南省")
        elif Premethod == "随机森林模型":
            T=math.floor(len(forpredata)/3)
            result= algorithms.RandomForest(StartYear, EndYear, PreStartYear, PreEndYear, T, pretype=savetype, n_estimators=50, city="云南省")
            
        if isinstance(result["preresult"],str):
            return {"prefromyear":None,"pretoyear":None,"preresult":"预测失败，请重新选择预测方法."}
        else:
            ypre=[]
            for k in range(len(propose.values)):
                power=result["preresult"][k]
                for n in range(len(rejectlsit)):
                    power=power+propose[rejectlsit[n]].values[k]
                ypre.append(power)
        result={"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre}
        return result


if __name__=="__main__":
    rejectlsit=["第一产业用电量","第二产业用电量"]
    proposedata="D:/lab/Yunnan_Pre/code_for_soft/联调/proposedata.csv"
    StartYear="2008"
    EndYear="2019"
    PreStartYear="2020"
    PreEndYear="2021"
    Premethod="支持向量机模型"
    result=ForIndustry(StartYear,EndYear,PreStartYear,PreEndYear,rejectlsit,proposedata,Premethod)
    



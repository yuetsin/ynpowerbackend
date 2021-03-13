# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 14:01:44 2021

@author: ZR_YL
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from scipy.optimize import leastsq
import math
#import predict_economic_LDM as predict
import algorithms.predict_inputdata as predict
from dao.interface import getData
import json
from algorithms.evaluation import RMSE,MAPE

def LDM(PreStartYear,PreEndYear,buildingarea,loaddensity,pretype="consumption",city="云南省"):
    
    def Density(n,Dlist,Plist):
        #n为所画片区，Dlist为对应的负荷密度，Plist为对应的建筑面积
        load=0
        for i in range(n):
            load=Dlist[i]*Plist[i]+load
        
        return load
    
    data1 = pd.read_csv(buildingarea, encoding="UTF-8")
    data2=pd.read_csv(loaddensity, encoding="UTF-8")
    columns=data1.columns
    columns2=data2.columns
    
    if len(columns) != len(columns2):
        return {"trainfromyear":None,"traintoyear":None,"trainresult":None,"prefromyear":None,"pretoyear":None,"preresult":"负荷密度和建筑密度列表不匹配，请重新上传。","MAPE":None,"RMSE":None}
    elif not (data1[columns[0]].values == data2[columns2[0]].values).all():
        return {"trainfromyear":None,"traintoyear":None,"trainresult":None,"prefromyear":None,"pretoyear":None,"preresult":"负荷密度和建筑密度年份不匹配，请重新上传。","MAPE":None,"RMSE":None}
    else:
        StartYear = str(data1[columns[0]].values[0])
        EndYear = str(data1[columns[0]].values[-1])
        #预测建筑用地数据
        building=predict.pre(data1.loc[:,[columns[0],columns[1]]],columns[1],int(PreStartYear),int(PreEndYear))
        for i in range(2,len(columns)):
            c=predict.pre(data1.loc[:,[columns[0],columns[i]]],columns[i],int(PreStartYear),int(PreEndYear))
            building=pd.merge(building,c,on=columns[0])
        
        #预测负荷密度
        density=predict.pre(data2.loc[:,[columns2[0],columns2[1]]],columns2[1],int(PreStartYear),int(PreEndYear))
        for i in range(2,len(columns2)):
            c=predict.pre(data2.loc[:,[columns2[0],columns2[i]]],columns2[i],int(PreStartYear),int(PreEndYear))
            density=pd.merge(density,c,on=columns2[0])
            
        
        #读取历史负荷数据
        period=int(EndYear)-int(StartYear)+1
        finaldata=[]
        name=[pretype]
        datajson = getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
        data=json.loads(datajson)
        finaldata.append(data)
    
        final=pd.DataFrame(finaldata,index=name)
        final=final.T
    
        trainx=[]
        start=0#训练集的起始位置
        for i in range(start,period):
            d=[building[columns[-1]].values[i]]
            b=[density[columns[-1]].values[i]]
            trainx.append(Density(1,d,b))
            
        trainy=[]
        trainyear=[]
        for j in range(period):
            if int(final.index.values[j]) in data1["year"].values[start:]:
                trainy.append(final[pretype].values[j])
                trainyear.append(final.index.values[j])
 
        prex=[]
        
        for a in range(period,len(building.values)):
            d=[building[columns[-1]].values[a]]
            b=[density[columns[-1]].values[a]]
            prex.append(Density(1,d,b))
        
        trainx=np.array(trainx).reshape(-1,1)
        trainy=np.array(trainy).reshape(-1,1)
        prex=np.array(prex).reshape(-1,1)

        #训练模型
        reg = LinearRegression().fit(trainx, trainy)
        prey = [x * reg.coef_[0][0] + reg.intercept_[0] for x in prex]
        
        pretrainy= [tx * reg.coef_[0][0] + reg.intercept_[0] for tx in trainx]
        ypre=np.array(prey).reshape(1,-1).squeeze()
        ytrain=np.array(pretrainy).reshape(1,-1)
        
        mape=MAPE(pretrainy,trainx)
        rmse=RMSE(pretrainy,trainx)
        
        #返回结果
        result={"bu":building,"trainfromyear":StartYear,"traintoyear":EndYear,"trainresult":ytrain.tolist(),"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre.tolist(),"MAPE":mape,"RMSE":rmse}
    return result

if __name__ == '__main__':

    PreStartYear = "2020"
    PreEndYear = "2029"
    buildingarea="D:/lab/Yunnan_Pre/data/yunnan_building.csv"
    loaddensity="D:/lab/Yunnan_Pre/data/yunnan_loaddensity.csv"
    result=LDM(PreStartYear,PreEndYear,buildingarea,loaddensity,pretype="consumption",city="云南省")
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 17:21:03 2021

@author: ZR_YL
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from scipy.optimize import leastsq
from algorithms.evaluation import RMSE,MAPE
import algorithms.io_csv as ic
from dao.interface import getData
import json 
import math





def Growth(StartYear,EndYear,PreStartYear,PreEndYear,pretype="全社会用电量",econamelist=["GDP"],city="云南省",planflag=0,plan=0):
    """
    

    Parameters
    ----------
    StartYear : TYPE
        DESCRIPTION.
    EndYear : TYPE
        DESCRIPTION.
    PreStartYear : TYPE
        DESCRIPTION.
    PreEndYear : TYPE
        DESCRIPTION.
    pretype : TYPE
        DESCRIPTION.
    econamelist : TYPE
        DESCRIPTION.
    city : TYPE, optional
        DESCRIPTION. The default is "云南省".
    planflag : TYPE, optional
        DESCRIPTION. The default is 0.
    plan : TYPE, optional
        DESCRIPTION. The default is 0.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    def func3(params, x):
        a, b, c = params
        return np.exp (a / x + b ) + c
    
    def error3(params, x, y):
        return func3(params, x) - y
    
    def slovePara3(x,y):
        p0 = [1, 0.02, 0]
        Para = leastsq(error3, p0, args=(x, y))
        return Para   
    




    if len(econamelist) !=1:
        return {"False":"请重新选择一个经济变量."}
    
    elif city=="云南省":
        name=[pretype]
        finaldata=[]
        
        #读取历史负荷数据
        datajson=getData("云南省_year_电力电量类", pretype, StartYear, EndYear)
        # print(datajson)
        data=json.loads(datajson)
        finaldata.append(data)
        
        #读取经济数据
        ecodatajson=getData("云南省_year_社会经济类", econamelist[0], StartYear, EndYear)
        ecodata=json.loads(ecodatajson)
        finaldata.append(ecodata)
        name.append(econamelist[0])
        
        #获取最终数据DataFrame
        final=pd.DataFrame(finaldata,index=name)
        final=final.T
        
        x = final[econamelist[0]].values
        y = final[pretype].values        #load


        x = x.reshape(-1,1)
        y = y.reshape(-1,1)


        #区分训练数据和预测数据
        num=len(x)
        testyear=math.floor(num/5)
        trainx=x[:num-testyear].squeeze()
        trainy=y[:num-testyear].squeeze()
        
        testx=x[num-testyear:]
        testy=y[num-testyear:]
        
        #建立模型
        Para = slovePara3(trainx,trainy)
        a, b, c = Para[0]
        
        testp = ic.getpred(testx,testyear,planflag,plan)
        testp = np.array(testp).T
        testpm = []
        for i in range(51):
            testpm.append(np.mean(testp[i]))
        testpmm = testpm.index(np.median(testpm))
        testpredx = testp[testpmm]
        testpredx = [k * testx[-1] for k in testpredx]
        testpredy = [np.exp (a / x + b ) + c for x in testpredx]


        trainyear=[]
        for t in testy:
            count=-1
            for d in final[pretype]:
                count+=1
                
                if t>d-5 and t<d+5:
                    # print("yes")
                    trainyear.append(final.index[count])
                    break
                
        #误差
        mape=MAPE(testpredy,testy)
        rmse=RMSE(testpredy,testy)
        
        #预测
        x=x.squeeze()
        y=y.squeeze()
        Parapre = slovePara3(x,y)
        ap, bp, cp = Parapre[0]
        
        
        preyear = np.arange(int(PreStartYear),int(PreEndYear)+1)
        year=len(preyear)
        p = ic.getpred(x,year,planflag,plan)
        p = np.array(p).T
        pm = []
        for i in range(51):
            pm.append(np.mean(p[i]))
        pmm = pm.index(np.median(pm))
        predx = p[pmm]
        predx = [k * x[-1] for k in predx]
            
        predy = [np.exp (ap / x0 + bp ) + cp for x0 in predx]
        predy=np.array(predy).squeeze()    

        #存储
        ytrain=np.array(testpredy).squeeze()
        ypre=np.array(predy).squeeze()
        result={"trainfromyear":trainyear[0],"traintoyear":trainyear[-1],"trainresult":ytrain.tolist(),"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre.tolist(),"MAPE":mape,"RMSE":rmse}
        return result
        
if __name__ == '__main__':
    StartYear="1990"
    EndYear="2019"
    PreStartYear="2020"
    PreEndYear="2022"
    pretype="全社会用电量"
    city="云南省"
    
    result=Growth(StartYear,EndYear,PreStartYear,PreEndYear,pretype,["GDP"],city)      
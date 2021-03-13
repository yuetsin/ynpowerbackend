# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 17:16:40 2021

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

def UnarylinearTime(StartYear,EndYear,PreStartYear,PreEndYear,pretype="consumption",city="云南省",planflag=0,plan=0):

    
    """一元一次外推"""
    
    if city=="云南省":
        name=[pretype]
        finaldata=[]
        
    
        #读取历史负荷数据
        datajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
        # print(datajson)
        data=json.loads(datajson)
        finaldata.append(data)
        
        
        #获取最终数据DataFrame
        final=pd.DataFrame(finaldata,index=name)
        final=final.T
        
        realyear = np.arange(int(StartYear),int(EndYear)+1)     

        final["time"]=realyear

        x = final["time"].values
        y = final[pretype].values        #load


        x = x.reshape(-1,1)
        y = y.reshape(-1,1)
    
        #区分训练数据和预测数据
        num=len(x)
        testyear=math.floor(num/5)
        trainx=x[:num-testyear]
        trainy=y[:num-testyear]
        
        testx=x[num-testyear:]
        testy=y[num-testyear:]
        
        reg = LinearRegression().fit(trainx, trainy)
        
        # reg = LinearRegression().fit(x, y)
        
        testp = ic.getpred(testx,testyear,planflag,plan)
        testp = np.array(testp).T
        testpm = []
        for i in range(51):
            testpm.append(np.mean(testp[i]))
        testpmm = testpm.index(np.median(testpm))
        testpredx = testp[testpmm]
        testpredx = [k * testx[-1] for k in testpredx]
        testpredy = [testx * reg.coef_[0][0] + reg.intercept_[0] for testx in testpredx]
        
        # loadp = reg.predict(testx)#趋势外推
        
        mape=MAPE(testpredy,testy)
        rmse=RMSE(testpredy,testy)



        trainyear=[]
        for t in testy:
            count=-1
            for d in final[pretype]:
                count+=1
                
                if t>d-5 and t<d+5:
                    # print("yes")
                    trainyear.append(final.index[count])
                    break
        
        
        
        
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
            
        predy = [x * reg.coef_[0][0] + reg.intercept_[0] for x in predx]
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
    PreEndYear="2021"
    pretype="consumption"
    city="云南省"
    
    result=UnarylinearTime(StartYear,EndYear,PreStartYear,PreEndYear,pretype,city)
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 14:57:22 2021

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
"""一元一次，已修改，未联调"""
def Unarylinear(StartYear,EndYear,PreStartYear,PreEndYear,pretype="全社会用电量",econamelist=["GDP"],city="云南省",planflag=0,plan=0):
    """
    

    Parameters
    ----------
    StartYear : str
        历史数据起始年份
    EndYear : str
        历史数据终止年份
    PreStartYear : str
        预测起始年份
    PreEndYear : str
        预测终止年份
    pretype : str
        预测类型："consumption"、"load"
    econamelist : list
        用到的社会经济类数据名称, e.g., ["GDP","人口"].
    city : str, optional
        预测城市. The default is "云南省".
    planflag : TYPE, optional
        是否有规划值，1代表有，0代表没有. The default is 0.
    plan : TYPE, optional
        规划指数值. The default is 0.

    Returns
    -------
    None.

    """
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
    pretype="全社会用电量"
    city="云南省"
    
    result=Unarylinear(StartYear,EndYear,PreStartYear,PreEndYear,pretype,["GDP"],city)

     

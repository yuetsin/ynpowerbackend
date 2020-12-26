# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 17:05:58 2020

@author: ZR_YL
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from scipy.optimize import leastsq


#预测各种经济数据,针对读取数据为数据接口的代码
def pre(data,name,fromyear,toyear):
    # print(data["GDP"].values)
    fromyear=int(fromyear)
    toyear=int(toyear)
        #数据表头为["year","value"]
    hisyear=data.index.values
    hisyear=list(map(int,hisyear))
    datastartyear=hisyear[0]
    datafinalyear=hisyear[-1]
    year=toyear-fromyear+1
    
    
    x = np.array(hisyear)
    y = data[name].values        #load
    
    x = x.reshape(-1,1)
    y = y.reshape(-1,1)

    #区分训练数据和预测数据
    num=len(x)
    if num>year+5:
        testyear=year
    else:
        testyear=5
    trainx=x[:num-testyear]
    trainy=y[:num-testyear]
    
    testx=x[num-testyear:]
    testy=y[num-testyear:]

    
    reg = LinearRegression().fit(trainx, trainy)
    
    # reg = LinearRegression().fit(x, y)
    testpredx=np.arange(trainx[-1]+1,trainx[-1]+1+testyear)
    testpredy = [testx * reg.coef_[0][0] + reg.intercept_[0] for testx in testpredx]
    
    # loadp = reg.predict(testx)#趋势外推
    
    # mape=MAPE(testpredy,testy)
    # rmse=RMSE(testpredy,testy)
    
    # print("MAPE=",mape)
    # print("RMSE=",rmse)
    
    
    reg1 = LinearRegression().fit(x, y)
    preyear = np.arange(fromyear,toyear+1).reshape(-1,1)
    
    predy = [x * reg1.coef_[0][0] + reg1.intercept_[0] for x in preyear]
    predy=np.array(predy).squeeze()

    finalyear=np.concatenate((x,preyear),axis=0)
    finallaod=np.concatenate((data[name],predy),axis=0)
    save=pd.DataFrame()
    save["year"]=finalyear.squeeze()
    save[name]=finallaod
    return save

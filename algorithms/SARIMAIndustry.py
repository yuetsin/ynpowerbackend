# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 16:41:54 2021

@author: ZR_YL
"""

import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
import math

import algorithms.predict_economic as preeco

from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json 




def SARIMAIndustry(StartYear,EndYear,PreStartYear,PreEndYear,pretype,city="云南省"):
    StartMonth="%s/1"%(StartYear)
    EndMonth="%s/12"%(EndYear)
    #读取月度数据
    monthdatajson=getData("yunnan_month_电力电量类", pretype, StartMonth, EndMonth)
    monthdata=json.loads(monthdatajson)
    pdmonthdata=pd.DataFrame(monthdata,index=[pretype])
    pdmonthdata=pdmonthdata.T
    #读取年度数据
    yeardatajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
    yeardata=json.loads(yeardatajson)
    pdyeardata=pd.DataFrame(yeardata,index=[pretype])
    pdyeardata=pdyeardata.T


    
    totalyear=int(EndYear)-int(StartYear)+1
    trainyear=math.floor(totalyear-totalyear*0.3)#2or5，意味着短期or中期
    train_num=trainyear*12
    train_data=pdmonthdata[pretype].values[:train_num]
    test_data=pdmonthdata[pretype].values[train_num:]
    
    
    mean = sum(train_data)/len(train_data) # 计算均值
    data_mean = [data - mean for data in train_data] # 得到去均值后的序列
    data_mean=np.array(data_mean)
    #做一阶差分差分，变量序列平稳.
    df_mean = pd.DataFrame(data_mean,index=pdmonthdata[pretype].values[:train_num],columns=['mean value'])
    df_mean_1 = np.diff(data_mean,1)
    # plt.plot(df_mean_1)
    # plt.show()
    
    # 进行ADF检验并打印结果
    adf_summary = ts.adfuller(np.array(df_mean_1).reshape(-1)) 
    # print(adf_summary)
    
    ###SARIMA-----ARIMA(p,d,q)(P,D,Q)s
    ### (p, d, q)是上述非季节性参数.(P, D, Q)遵循相同的定义.但适用于时间序列的季节分量. 术语s是时间序列的周期（季度为4 ,年度为12 ,等等）.
    ###https://blog.csdn.net/weixin_39479282/article/details/89513624
    
    ##select the best parameter proup of SARIMA, using AIC （Akaike信息标准）
    
    # Define the p, d and q parameters to take any value between 0 and 2
    p=q=P=Q=range(0,3)#短期取得是（0,3）
    d=D=1#短期取得是1
    parameters = itertools.product(p,q,P,Q)
    parameters_list = list(parameters)
    
    
    warnings.filterwarnings("ignore")
    # param_best=tuple()
    # param_seasonal_best=tuple()
    result = []
    best_aic = float("inf")
    for parameters in parameters_list:
        try:
            model = sm.tsa.statespace.SARIMAX(df_mean_1,
                                            order=(parameters[0],d,parameters[1]),
                                            seasonal_order=(parameters[2], D, parameters[3], 12)).fit(disp=-1)
            # print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue
        aic = model.aic
        if aic < best_aic:
            best_aic = aic
            best_param = parameters
        result.append([parameters, model.aic])
    
    # result_table = pd.DataFrame(result)
    # result_table.columns = ['parameters', 'aic']
    # print(result_table.sort_values(by='aic', ascending=True).head())
    
    ###prediction   
    best_model=sm.tsa.statespace.SARIMAX(train_data,
                                            order=(best_param[0],d,best_param[1]),
                                            seasonal_order=(best_param[2], D, best_param[3], 12)).fit(disp=-1)
    
    test_predict=best_model.forecast(steps=len(test_data))
    
    #将月度数据转化为年度数据
    def month_to_year(test_predict):
        finalpredict=[]
        loadsum=0
        for i in range(len(test_predict)):
            if ((i+1)%12==0) and loadsum!=0:
                loadsum=loadsum+test_predict[i]
                finalpredict.append(loadsum)
                loadsum=0
            else:
                loadsum=loadsum+test_predict[i]
        finalpredict=np.array(finalpredict)
        return finalpredict
    
    finalpredict=month_to_year(test_predict)
    finaltrue=np.flipud(pdyeardata[pretype].values[-1:-(len(finalpredict)+1):-1])
    mape=MAPE(finalpredict,finaltrue)
    rmse=RMSE(finalpredict,finaltrue)
    
    trainyear=[]
    for t in finaltrue:
        for year, data in pdyeardata.iterrows():
            if t>data[pretype]-5 and t<data[pretype]+5:
                trainyear.append(year)
                break
    ytrain=np.array(finalpredict)
    
    #预测

    
    outputlen=int(PreEndYear)-int(PreStartYear)+1
    traindata=pdmonthdata[pretype].values
    best_model=sm.tsa.statespace.SARIMAX(traindata,
                                            order=(best_param[0],d,best_param[1]),
                                            seasonal_order=(best_param[2], D, best_param[3], 12)).fit(disp=-1)
    predict=best_model.forecast(steps=outputlen*12)
    finalpredict=month_to_year(predict)
    ypre=np.array(finalpredict)
    
    
    result={"trainfromyear":trainyear[0],"traintoyear":trainyear[-1],"trainresult":ytrain.tolist(),"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre.tolist(),"MAPE":mape,"RMSE":rmse}
    return result

if __name__ == '__main__':
    pretype="第一产业用电量"
    StartYear="2008"
    EndYear="2019"
    PreStartYear="2020"
    PreEndYear="2021"
    result=SARIMAIndustry(StartYear,EndYear,PreStartYear,PreEndYear,pretype,city="云南省")
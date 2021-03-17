# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 16:41:37 2021

@author: ZR_YL
"""



import sklearn
from sklearn.svm import SVR
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from PyEMD import EMD
from sklearn.multioutput import MultiOutputRegressor
import algorithms.predict_economic as preeco

from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json 
import math


def EEMDIndustry(StartYear,EndYear,PreStartYear,PreEndYear,pretype,city="云南省"):



    #读取年度数据
    yeardatajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
    yeardata=json.loads(yeardatajson)
    pdyeardata=pd.DataFrame(yeardata,index=[pretype])
    pdyeardata=pdyeardata.T
    
    totalyear=int(EndYear)-int(StartYear)+1
    timestep=int(PreEndYear)-int(PreStartYear)+1
    
    delay=2
    trainyear=math.floor(totalyear-totalyear*0.3)#2or5，意味着短期or中期
    testyear=trainyear+delay
    
    
    
    train_x=pdyeardata[pretype].values[:trainyear]
    train_y=pdyeardata[pretype].values[trainyear:trainyear+timestep]
    train_x=train_x.reshape(1,-1)
    train_y=train_y.reshape(1,-1)
    
    test_x=pdyeardata[pretype].values[delay:testyear]
    test_y=pdyeardata[pretype].values[testyear:testyear+timestep]
    test_x=test_x.reshape(1,-1)
    test_y=test_y.reshape(1,-1)
    
    testdata=pdyeardata[pretype].values
    finalpre=np.array(np.flipud(testdata[-1:-(trainyear+1):-1])).reshape(1,-1)
    
    emd = EMD()
    IMFs = emd(train_y.squeeze())#
    
    svr=SVR(kernel="linear",gamma="scale",C= 0.001)#kernel="linear","poly"
    multi_model = MultiOutputRegressor(svr)
    multi_model.fit(train_x,IMFs)
    predict_imf=multi_model.predict(test_x) 
    predict_imf_train=multi_model.predict(train_x) 
    final_imf=multi_model.predict(finalpre) 
    
    clf = SVR(kernel="linear")
    multi_model_c = MultiOutputRegressor(clf)
    multi_model_c.fit(IMFs, train_y)
    
    predict=multi_model_c.predict(predict_imf)
    mape=MAPE(predict,test_y)
    rmse=RMSE(predict,test_y)
    
    
    predict_train=multi_model_c.predict(predict_imf_train)
    
    final_result=multi_model_c.predict(final_imf)
    
    # trainfromyear=pdyeardata[]
    # trainendyear=
    
    ytrain=predict_train.flatten()
    ypre=final_result.reshape(-1,1).squeeze()
    
    result={"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre.tolist(),"MAPE":mape,"RMSE":rmse}
    return result

if __name__ == '__main__':
    pretype="电石用电量"
    StartYear="2008"
    EndYear="2019"
    PreStartYear="2020"
    PreEndYear="2021"
    
    result=EEMDIndustry(StartYear,EndYear,PreStartYear,PreEndYear,pretype,city="云南省")
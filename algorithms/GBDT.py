# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:31:20 2020

@author: ZR_YL
"""




import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
import math
from algorithms.train_test_set import generate_data,inverse_data

from sklearn.metrics import r2_score
import xgboost as xgb
from algorithms.interface import getData
import json 
from algorithms.evaluation import RMSE,MAPE


"""GBDT,未联调，已修改"""




def GBDT(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype="consumption",city="云南省",LearningRate=0.5, MaxDepth=200, NumberofEstimators=5000):

    #读取数据，确定参数
    name=[pretype]
    finaldata=[]
    outputlen=int(PreEndYear)-int(PreStartYear)+1

    datajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
    data=json.loads(datajson)
    finaldata.append(data)
    final=pd.DataFrame(finaldata,index=name)
    final=final.T

    test_size=0#测试数据集应当取0.3才可以
    X,y=generate_data(final,timestep,outputlen,test_size=test_size,if_norm="no")

    gbdt=xgb.XGBRegressor(max_depth=MaxDepth, learning_rate=LearningRate, n_estimators=NumberofEstimators, 
                  silent=True, objective='reg:linear', booster='gblinear', n_jobs=50, 
                  nthread=None, gamma=0, min_child_weight=1, max_delta_step=0, subsample=1, 
                  colsample_bytree=1, colsample_bylevel=1, reg_alpha=0, reg_lambda=1,
                  scale_pos_weight=1, base_score=0.5, random_state=0, seed=None,
                  missing=None, importance_type='gain')#

    multi_model = MultiOutputRegressor(gbdt)
    multi_model.fit(X["train"],y["train"])

    testdata=final.values
    num=len(X["train"])
    selet=int(np.floor(num/2))
    testinput=X["train"][selet:,:]
    testoutput=y["train"][selet:,:]

    x_pre=np.array(np.flipud(testdata[-1:-(timestep+1):-1])).reshape(1,-1)
    
    y1_gbdt=multi_model.predict(testinput)
    y1_gbdt_real=np.array(y1_gbdt).reshape(-1,1)
    y1_real=np.array(testoutput).reshape(-1,1)

    mape=MAPE(y1_gbdt_real,y1_real)
    rmse=RMSE(y1_gbdt_real,y1_real)

    ytrain=y1_gbdt[-1]
    trainyear=[]
    for t in testoutput[-1]:
        count=-1
        for d in final[pretype]:
            count+=1
            if t>d-1 and t<d+1:
                trainyear.append(final.index[count])
                break
    pre=multi_model.predict(x_pre)
    ypre=np.array(pre).flatten()
    result={"trainfromyear":trainyear[0],"traintoyear":trainyear[-1],"trainresult":ytrain,"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre,"MAPE":mape,"RMSE":rmse}
    #保存
    return result

StartYear="1990"
EndYear="2019"
PreStartYear="2020"
PreEndYear="2021"
timestep=10
pretype="consumption"
city="云南省"

result=GBDT(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype,city)


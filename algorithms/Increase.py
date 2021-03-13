# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:10:20 2021

@author: ZR_YL
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import math
from algorithms.train_test_set import generate_data,inverse_data

from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json 

"""增长率法,不可以组合预测"""

def Increase(StartYear,EndYear,PreStartYear,PreEndYear,rate,pretype="consumption",city="云南省"):
    if city == "云南省":
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
        preyear  = np.arange(int(PreStartYear),int(PreEndYear)+1)

        final["time"]=realyear

        x = final[pretype].values        #load

        data = x[-1]
        
        
        ypre = [data*(1+rate)**(i+1) for i in range(len(preyear))]
        ypre=np.array(ypre)


        result={"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre.tolist()}
        return result


StartYear="1990"
EndYear="2019"
PreStartYear="2020"
PreEndYear="2022"
pretype="consumption"
city="云南省"

result=Increase(StartYear,EndYear,PreStartYear,PreEndYear,0.1,pretype,city) 
        
        
        
        
        
        
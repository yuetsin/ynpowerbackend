# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 12:24:04 2021

@author: ZR_YL
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from dao.interface import getData
import json
from datetime import datetime 


def Outlier(StartYear,EndYear, pretype="consumption",city="云南省"):
    #读取数据
    name=[pretype]
    finaldata=[]
    year=np.arange(int(StartYear),int(EndYear)+1,1)
    
    datajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
    data=json.loads(datajson)
    finaldata.append(data)
    final=pd.DataFrame(finaldata,index=name)
    final=final.T
    
    t=final[pretype]
    tnp=np.array(t.values)
    sigma=t[abs(t-t.mean())> 3*t.std()]
    out=sigma.dropna(how="all")#异常值
    index_out=np.where(tnp==i)[0]#异常值下标
    outyear=[]
    outcorrect=[]
    for i in index_out:
        outyear.append(year[i])
        if i==0:
            correct=(tnp[i+1]+tnp[i])/2
        elif i==len(tnp)-1:
            correct=(tnp[i]+tnp[i-1])/2
        else:
            correct=(tnp[i+1]+tnp[i-1])/2
        outcorrect=correct
        
        
    result={"outlier":out.values,"year":outyear, "correction":outcorrect}
    return result

if __name__ == '__main__':
    StartYear="1990"
    EndYear="2019"
    o=Outlier(StartYear,EndYear, pretype="consumption",city="云南省")

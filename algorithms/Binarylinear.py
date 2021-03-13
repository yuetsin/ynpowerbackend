# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 16:37:57 2021

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




def Binarylinear(StartYear,EndYear,PreStartYear,PreEndYear,econamelist,pretype="consumption",city="云南省",planflag1=0,plan1=0,planflag2=0,plan2=0):
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
    planflag1 : TYPE, optional
        DESCRIPTION. The default is 0.
    plan1 : TYPE, optional
        DESCRIPTION. The default is 0.
    planflag2 : TYPE, optional
        DESCRIPTION. The default is 0.
    plan2 : TYPE, optional
        DESCRIPTION. The default is 0.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    def madd(X,Y):
        Z = []
        lenX = len(X)
        for i in range(lenX):
                Z.append(X[i][0]+Y[i][0])
        return Z
    
    
    if len(econamelist) !=2:
        return {"False":"请重新选择两个经济变量."}
    elif city=="云南省":
        name=[pretype]
        finaldata=[]
        period=int(PreEndYear)-int(PreStartYear)+1
        
        #读取历史负荷数据
        datajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
        # print(datajson)
        data=json.loads(datajson)
        finaldata.append(data)
        
        #读取经济数据
        for i in range(2):
            ecodatajson=getData("yunnan_year_社会经济类", econamelist[i], StartYear, EndYear)
            ecodata=json.loads(ecodatajson)
            finaldata.append(ecodata)
            name.append(econamelist[i])
        
        #获取最终数据DataFrame
        final=pd.DataFrame(finaldata,index=name)
        final=final.T  
        
        

        x1 = final[econamelist[0]].values
        x2 = final[econamelist[1]].values
        y = final[pretype].values        #load


        x1 = x1.reshape(-1,1)
        x2 = x2.reshape(-1,1)
        xx=np.concatenate((x1,x2),axis=1)
        y = y.reshape(-1,1)


        #区分训练数据和预测数据
        num=len(y)
        testyear=math.floor(num/5)
        trainx=xx[:num-testyear]
        trainy=y[:num-testyear]
        
        testx=xx[num-testyear:]
        testy=y[num-testyear:]
        
        # reg = LinearRegression().fit(trainx, trainy)
        
        reg = LinearRegression().fit(xx, y)
        
        testp1 = ic.getpred(testx[:,0],testyear,planflag1,plan1)
        testp1 = np.array(testp1).T
        testpm1 = []
        for i in range(51):
            testpm1.append(np.mean(testp1[i]))
            
        testpmm1 = testpm1.index(np.median(testpm1))
        testpredx1 = testp1[testpmm1]
        testpredx1 = [k * testx[:,0][-1] for k in testpredx1]
        testpredy1 = [testx[:,0] * reg.coef_[0][0] + reg.intercept_[0] for testx[:,0] in testpredx1]
        
        
        
        testp2 = ic.getpred(testx[:,1],testyear,planflag2,plan2)
        testp2 = np.array(testp2).T
        testpm2 = []
        for i in range(51):
            testpm2.append(np.mean(testp2[i]))
        testpmm2 = testpm2.index(np.median(testpm2))
        testpredx2 = testp2[testpmm2]
        testpredx2 = [k * testx[:,1][-1] for k in testpredx2]
        testpredy2 = [testx[:,1] * reg.coef_[0][1] for testx[:,1] in testpredx2]
        
        testpredy = madd(testpredy1 , testpredy2)
        # testpredy=np.array(testpredy).squeeze()
        
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


        """预测"""       
        preyear = np.arange(int(PreStartYear),int(PreEndYear)+1)
        year=len(preyear)
        p1 = ic.getpred(xx[:,0],year,planflag1,plan1)
        p1 = np.array(p1).T
        pm1 = []
        for i in range(51):
            pm1.append(np.mean(p1[i]))
            
        pmm1 = pm1.index(np.median(pm1))
        predx1 = p1[pmm1]
        predx1 = [k * xx[:,0][-1] for k in predx1]
        predy1 = [xx[:,0] * reg.coef_[0][0] + reg.intercept_[0] for xx[:,0] in predx1]
        
        
        
        p2 = ic.getpred(xx[:,1],year,planflag2,plan2)
        p2 = np.array(p2).T
        pm2 = []
        for i in range(51):
            pm2.append(np.mean(p2[i]))
            
        pmm2 = pm2.index(np.median(pm2))
        predx2 = p2[pmm2]
        predx2 = [k * xx[:,1][-1] for k in predx2]
        predy2 = [xx[:,1] * reg.coef_[0][1] for xx[:,1] in predx2]
        
        predy = madd(predy1 , predy2)
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
    PreEndYear="2025"
    pretype="consumption"
    city="云南省"
    
    result=Binarylinear(StartYear,EndYear,PreStartYear,PreEndYear,["GDP","energyproduct"],pretype,city)


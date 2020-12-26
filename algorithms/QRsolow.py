# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 12:54:03 2020

@author: ZR_YL
"""

import numpy as np
import pandas as pd

from sklearn import linear_model
import statsmodels.api as sm
import statsmodels.formula.api as smf

from algorithms.predict_economic import pre as predict
from algorithms.evaluation import RMSE,MAPE
from algorithms.interface import getData
import json

"""扩展索洛分位数回归"""


def QRsolow(hisfromyear,histoyear,fromyear,toyear,quatile=0.95,pretype="consumption",econamelist=["GDP"],city="云南省"):
    """
    

    Parameters
    ----------
    hisfromyear : str
        历史数据起始年份
    histoyear : str
        历史数据终止年份
    fromyear : str
        预测起始年份
    toyear : str
        预测终止年份
    pretype : str
        预测类型："consumption"、"load"
    quatile : float
        分位数,默认为0.95
    econamelist : list
        选取的经济数据名称列表
    city : str
        选择城市，默认云南省

    Returns
    -------
    "trainfromyear":hisfromyear  
        
    "traintoyear":histoyear
    
    "trainresult":ytrain,  array
        训练结果
    "prefromyear":fromyear
    
    "pretoyear":toyear
    
    "preresult":ypre,  array
        预测结果
    "MAPE":mape, float
        
    "RMSE":rmse, float
        

    """
    def get_coef(data,pretype,econamelist,quatile):
        #获得分位数回归线性关系
        #注意xnamelist 最多只能容纳5个变量,yname是str
        #n=len(xnamelist)
        n=len(econamelist)
        if n==1:
           mod = smf.quantreg('%s ~ %s'%(pretype,econamelist[0]), data) 
        elif n==2:
            mod = smf.quantreg('%s ~ %s+%s'%(pretype,econamelist[0],econamelist[1]), data) 
        elif n==3:
            mod = smf.quantreg('%s ~ %s+%s+%s'%(pretype,econamelist[0],econamelist[1],econamelist[2]), data) 
        elif n==4:
            mod = smf.quantreg('%s ~ %s+%s+%s+%s'%(pretype,econamelist[0],econamelist[1],econamelist[2],econamelist[3]), data)
        elif n==5:
            mod = smf.quantreg('%s ~ %s+%s+%s+%s+%s'%(pretype,econamelist[0],econamelist[1],econamelist[2],econamelist[3],econamelist[4]), data)
        res = mod.fit(q=quatile)
        # print(res.summary())
        #返回分位点，截距，各个参数系数 和 各个参数lb,ub
        return quatile,res.params['Intercept'],res.params[econamelist],res.conf_int().loc[econamelist]
    
    def predict(data,intercept,coef,quatile,econamelist):
        #这里的data只有x没有y
        n=len(econamelist)
        pre=[intercept]*len(data.values)
        for i in range(n):
            pre=pre+coef[econamelist[i]]*data[econamelist[i]].values
        pre=np.exp(pre)
        return pre    
    
    
    
    #判断经济因素数量是否合适
    if len(econamelist)>5:
        delnum=len(econamelist)-5
        print("经济因素选取不应超出5个,请删去%s个,再重新预测。"%delnum)
    elif city=="云南省":
        name=[pretype]
        finaldata=[]
        period=toyear-fromyear+1
        
        #读取历史负荷数据
        datajson=getData("yunnan_year", pretype, hisfromyear, histoyear)
        data=json.loads(datajson)
        finaldata.append(data)
        
        #读取经济数据
        for i in range(len(econamelist)):
            
            ecodatajson=getData("yunnan_year", econamelist[i], hisfromyear, histoyear)
            ecodata=json.loads(ecodata)
            finaldata.append(ecodata)
            name.append(econamelist[i])
        
        #获取最终数据DataFrame
        final=pd.DataFrame(finaldata,index=name)
        final=final.T
        
        #取对数
        logfinal=data.apply(np.log)
        
        #预测经济数据
        eco=predict.pre(logfinal.loc[:,econamelist[0]],econamelist[0],fromyear,toyear)
        for j in range(1,len(econamelist)):
            c=predict.pre(logfinal.loc[:,econamelist[j]],econamelist[j],fromyear,toyear)
            eco=pd.merge(eco,c,on="year")  
        
        
        #预测
        q,b,k,lbub=get_coef(logfinal,name,pretype,quatile)
        y=predict(eco,b,k,q,econamelist)

        #求训练集误差mape，rmse
        ytrain=y[:len(y)-period]
        ytraintrue=data[pretype].values[:len(y)-period]
        mape=MAPE(ytrain,ytraintrue)
        rmse=RMSE(ytrain,ytraintrue)
        print("MAPE=",mape)
        print("RMSE=",rmse)    
        ypre=y[len(y)-period:]
        
        
        #返回结果
        return {"trainfromyear":hisfromyear,"traintoyear":histoyear,"trainresult":ytrain,
                "prefromyear":fromyear,"pretoyear":toyear,"preresult":ypre,"MAPE":mape,"RMSE":rmse}
    else:
        return {"False":"暂不支持其他地区预测"}

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
import algorithms.predict_economic as preeco

from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json

"""扩展索洛分位数回归"""


def ESQRM(StartYear,EndYear,PreStartYear,PreEndYear,quatile=0.95,pretype="consumption",econamelist=["GDP"],city="云南省", kind = "电力电量类", grain="year"):
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
    quatile : float
        分位数,默认为0.95
    econamelist : list
        选取的经济数据名称列表
    city : str
        选择城市，默认云南省

    Returns
    -------
    "trainfromyear":StartYear  
        
    "traintoyear":EndYear
    
    "trainresult":ytrain,  array
        训练结果
    "prefromyear":PreStartYear
    
    "pretoyear":PreEndYear
    
    "preresult":ypre,  array
        预测结果
    "MAPE":mape, float
        
    "RMSE":rmse, float
        

    """
    def get_coef(data,pretype,econamelist,quatile):
        #获得分位数回归线性关系
        #注意econamelist 最多只能容纳5个变量,yname是str
        n=len(econamelist)
        # print("num",n)
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
        period=int(PreEndYear)-int(PreStartYear)+1
        
        #读取历史负荷数据
        datajson=getData("yunnan_year_社会经济类", pretype, StartYear, EndYear)
        # print(datajson)
        data=json.loads(datajson)
        finaldata.append(data)
        
        #读取经济数据
        for i in range(len(econamelist)):
            
            ecodatajson=getData("yunnan_year_社会经济类", econamelist[i], StartYear, EndYear)
            ecodata=json.loads(ecodatajson)
            finaldata.append(ecodata)
            name.append(econamelist[i])
        
        #获取最终数据DataFrame
        final=pd.DataFrame(finaldata,index=name)
        final=final.T
        
        #取对数
        logfinal=final.apply(np.log)
    
        #预测经济数据
        # print(logfinal[econamelist[0]].to_frame().column)
        eco=preeco.pre(logfinal,econamelist[0],PreStartYear,PreEndYear)
        for j in range(1,len(econamelist)):
            c=preeco.pre(logfinal,econamelist[j],PreStartYear,PreEndYear)
            eco=pd.merge(eco,c,on="year")  
        
        
        #预测
        q,b,k,lbub=get_coef(logfinal,pretype,econamelist,quatile)
        y=predict(eco,b,k,q,econamelist)
    
        #求训练集误差mape，rmse
        ytrain=y[:len(y)-period]
        ytraintrue=final[pretype].values[:len(y)-period]
        mape=MAPE(ytrain,ytraintrue)
        rmse=RMSE(ytrain,ytraintrue)
        # print("MAPE=",mape)
        # print("RMSE=",rmse)    
        ypre=y[len(y)-period:]


        #返回结果
        result={"trainfromyear":StartYear,"traintoyear":EndYear,"trainresult":list(ytrain),"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":list(ypre),"MAPE":mape,"RMSE":rmse}
    else:
        result={"False":"暂不支持其他地区预测"}
    return result

#result=ESQRM("1995","2019","2020","2021",quatile=0.95,pretype="consumption",econamelist=["GDP"],city="云南省")

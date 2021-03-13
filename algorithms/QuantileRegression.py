# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:19:09 2020

@author: ZR_YL
"""


import numpy as np
import pandas as pd

from sklearn import linear_model
import statsmodels.api as sm
import statsmodels.formula.api as smf
from train_test_set import generate_data,inverse_data
import predict_economic as preeco
from evaluation import RMSE,MAPE
from interface import getData
import json 

"""分位数回归，未联调，已修改"""

def QuantileRegression(StartYear,EndYear,PreStartYear,PreEndYear,quatile=0.95,pretype="consumption",econamelist=["GDP"],city="云南省"):
    #首先需要回归得到未来的经济数据

    def get_coef(data,xnamelist,yname,quatile):
        #获得分位数回归线性关系
        #注意xnamelist 最多只能容纳5个变量,yname是str
        n=len(xnamelist)
        print(yname, xnamelist)
        if n==1:
           mod = smf.quantreg('%s ~ %s'%(yname,xnamelist[0]), data) 
        elif n==2:
            mod = smf.quantreg('%s ~ %s+%s'%(yname,xnamelist[0],xnamelist[1]), data) 
        elif n==3:
            mod = smf.quantreg('%s ~ %s+%s+%s'%(yname,xnamelist[0],xnamelist[1],xnamelist[2]), data) 
        elif n==4:
            mod = smf.quantreg('%s ~ %s+%s+%s+%s'%(yname,xnamelist[0],xnamelist[1],xnamelist[2],xnamelist[3]), data)
        elif n==5:
            mod = smf.quantreg('%s ~ %s+%s+%s+%s+%s'%(yname,xnamelist[0],xnamelist[1],xnamelist[2],xnamelist[3],xnamelist[4]), data)
        res = mod.fit(q=quatile)
        print(res.summary())
        #返回分位点，截距，各个参数系数 和 各个参数lb,ub
        return quatile,res.params['Intercept'],res.params[xnamelist],res.conf_int().loc[xnamelist]

    def predict(data,intercept,coef,quatile,xnamelist):
        #这里的data只有x没有y
        n=len(xnamelist)
        pre=[intercept]*len(data.values)
        for i in range(n):
            pre=pre+coef[xnamelist[i]]*data[xnamelist[i]].values
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
        datajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
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
        
        #预测经济数据
        # print(logfinal[econamelist[0]].to_frame().column)
        eco=preeco.pre(final,econamelist[0],PreStartYear,PreEndYear)
        for j in range(1,len(econamelist)):
            c=preeco.pre(final,econamelist[j],PreStartYear,PreEndYear)
            eco=pd.merge(eco,c,on="year")  
    
    
        q,b,k,lbub=get_coef(final,econamelist,pretype,0.95)
        
        y=predict(eco,b,k,q,econamelist)
        #求mape，rmse
        ytrain=y[:len(y)-period]
        ytraintrue=final[pretype].values[:len(y)-period]
        mape=MAPE(ytrain,ytraintrue)
        rmse=RMSE(ytrain,ytraintrue)
        ypre=y[len(y)-period:]


        #返回结果
        result={"trainfromyear":StartYear,"traintoyear":EndYear,"trainresult":ytrain.tolist(),"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre.tolist(),"MAPE":mape,"RMSE":rmse}
    else:
        result={"False":"暂不支持其他地区预测"}
    return result

if __name__ == '__main__':

    result=QuantileRegression("1995","2019","2020","2021",quatile=0.95,pretype="consumption",econamelist=["GDP"],city="云南省")
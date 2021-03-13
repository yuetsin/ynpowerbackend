# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:59:16 2020

@author: ZR_YL
"""



import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from algorithms.train_test_set import generate_data,inverse_data

from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json 
"""
改进灰色预测模型
"""
def GPRM(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype="consumption",city="云南省"):
    def improve_GM(x,n):
        '''
        改进灰色预测
        x：序列，numpy对象
        n:需要往后预测的个数
        '''    
        x1 = x.cumsum()#一次累加  
        z1 = (x1[:len(x1) - 1] + x1[1:])/2.0#紧邻均值  
        z1 = z1.reshape((len(z1),1))  
        B = np.append(-z1,np.ones_like(z1),axis=1)  
        Y = x[1:].reshape((len(x) - 1,1))
        #a为发展系数 b为灰色作用量
        [[a],[b]] = np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), Y)#计算参数  
        result = (x[0]-b/a)*np.exp(-a*(n-1))-(x[0]-b/a)*np.exp(-a*(n-2))  
        S1_2 = x.var()#原序列方差
        e = list()#残差序列
        for index in range(1,x.shape[0]+1):
            predict = (x[0]-b/a)*np.exp(-a*(index-1))-(x[0]-b/a)*np.exp(-a*(index-2))
            e.append(x[index-1]-predict)
        S2_2 = np.array(e).var()#残差方差
        C = S2_2/S1_2#后验差比
        if C<=0.35:
            assess = '后验差比<=0.35，模型精度等级为好'
        elif C<=0.5:
            assess = '后验差比<=0.5，模型精度等级为合格'
        elif C<=0.65:
            assess = '后验差比<=0.65，模型精度等级为勉强'
        else:
            assess = '后验差比>0.65，模型精度等级为不合格'
        #预测数据
        predict = list()
        for index in range(x.shape[0]+1,x.shape[0]+n+1):
            predict.append((x[0]-b/a)*np.exp(-a*(index-1))-(x[0]-b/a)*np.exp(-a*(index-2)))
        predict = np.array(predict)
        return predict,a,b,assess
    def GMpre(x,n,a,b):
        predict = list()
        for index in range(x.shape[0]+1,x.shape[0]+n+1):
            predict.append((x[0]-b/a)*np.exp(-a*(index-1))-(x[0]-b/a)*np.exp(-a*(index-2)))
        predict = np.array(predict)
        return predict


    if timestep > (int(EndYear)-int(StartYear)+1):
        return {"trainfromyear":None,"traintoyear":None,"trainresult":None,"prefromyear":None,"pretoyear":None,"preresult":"训练步长过大，请调整后重试.","MAPE":None,"RMSE":None}
    else:

        """负荷预测"""
        name=[pretype]
        finaldata=[]
        
        outputlen=int(PreEndYear)-int(PreStartYear)+1
        
        #读取历史负荷数据
        datajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
        # print(datajson)
        data=json.loads(datajson)
        finaldata.append(data)
        final=pd.DataFrame(finaldata,index=name)
        final=final.T
    
        
        datafinalyear=int(EndYear)
        trainyear=timestep
        testyear=int(PreEndYear)-int(PreStartYear)+1
        
        y = final.values  
        y = y.reshape(-1,1)
        
        #区分训练数据和预测数据
        num=len(y)
        #训练集
        trainx=y[num-testyear-1-trainyear:num-testyear-1].squeeze()
        trainy=y[num-testyear-1:].squeeze()
        #测试集
        testx=y[num-testyear-trainyear:num-testyear].squeeze()
        testy=y[num-testyear:].squeeze()
        #开始训练
        trainpre,a,b,assess=improve_GM(trainx,testyear)
        #获得测试结果
        testpre=GMpre(testx,testyear,a,b)
        
        #获得最终预测
        testpredx=np.array(np.flipud(y[-1:-(trainyear+1):-1]))
        finalpre=GMpre(testpredx,testyear,a,b)
        
        mape=MAPE(testpre,testy)
        rmse=RMSE(testpre,testy)
    
        
        ypre=finalpre.reshape(1,-1).squeeze()
    
        trainyear=[]
        for t in testy:
            count=-1
            for d in final[pretype]:
                count+=1
                
                if t>d-5 and t<d+5:
                    # print("yes")
                    trainyear.append(final.index[count])
                    break
    
        result={"trainfromyear":trainyear[0],"traintoyear":trainyear[-1],"trainresult":trainpre.tolist(),"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre.tolist(),"MAPE":mape,"RMSE":rmse}
        #保存
        return result
if __name__ == '__main__':
    StartYear="1990"
    EndYear="2019"
    PreStartYear="2020"
    PreEndYear="2029"
    timestep=15
    pretype="consumption"
    city="云南省"
    result=GPRM(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype="consumption",city="云南省")


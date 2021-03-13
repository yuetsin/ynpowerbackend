# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 15:08:55 2021

@author: ZR_YL
"""


import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import algorithms.predict_economic as preeco
from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json
import math 



def PCAindustry(StartYear,EndYear,PreStartYear,PreEndYear,pretype,econamelist,city="云南省"):
    
    if city=="云南省":
        name=[pretype]
        finaldata=[]
        period=int(PreEndYear)-int(PreStartYear)+1
        historyyear=np.arange(int(StartYear),int(EndYear)+1)
        
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
        final["Year"]=historyyear
        
        #预测经济数据
        # print(logfinal[econamelist[0]].to_frame().column)
        eco=preeco.pre(final,econamelist[0],PreStartYear,PreEndYear)
        for j in range(1,len(econamelist)):
            c=preeco.pre(final,econamelist[j],PreStartYear,PreEndYear)
            eco=pd.merge(eco,c,on="year")  

        Index=eco.columns[1:].tolist()#经济特征名称
        


        ##对特征数据进行归一化处理
        scaler = StandardScaler()
        scaler.fit(eco[Index].values)
        Data_eco_scaler = scaler.transform(eco[Index].values)
        Data_eco_scaler=pd.DataFrame(data=Data_eco_scaler,columns=Index)

        Data_eco_scaler["Year"]=eco["year"].values#归一化后的特征数据
        
        
        #获得训练数据集合测试数据集
                
        train_start_year=int(StartYear)
        train_end_year=int(StartYear)+math.ceil(len(historyyear)*0.7)
        test_start_year=int(StartYear)+math.ceil(len(historyyear)*0.7)
        test_end_year=int(EndYear)



        x_train=Data_eco_scaler.loc[Data_eco_scaler["Year"].isin(range(train_start_year,train_end_year+1))]
        y_train=final.loc[final["Year"].isin(range(train_start_year,train_end_year+1))]
        x_test=Data_eco_scaler.loc[Data_eco_scaler["Year"].isin(range(test_start_year,test_end_year+1))]
        y_test=final.loc[final["Year"].isin(range(test_start_year,test_end_year+1))]


        #获取合适的PCA维度
        pca = PCA(0.9)
        principalComponents = pca.fit_transform(Data_eco_scaler[Index].values)
        n_components = pca.n_components_#得到PCA的维度
        #print("n_components = ",pca.n_components_)
        
        #进行PCA分析
        pca = PCA(n_components)
        
        pca.fit(x_train[Index].values)
        
        x_train_pca=pca.transform(x_train[Index].values)
        y_train_pca=y_train[pretype]
        x_test_pca=pca.transform(x_test[Index].values)
        y_test_pca=y_test[pretype]
        
        #建立线性回归
        pca_model = LinearRegression()
        pca_model.fit(x_train_pca, y_train_pca)
        pca_predict = pca_model.predict(x_test_pca)
        
        #评价指标
        
        rmse = RMSE(pca_predict,y_test_pca)
        mape = MAPE(pca_predict,y_test_pca)
        
        #保存训练结果
        # trainyear=[]
        # for t in y_test_pca:
        #     for d in final.values:
        #         if t>d[1]-5 and t<d[1]+5:
        #             trainyear.append(d[0])
        #             break

        trainyear=[]
        for t in y_test_pca:
            count=-1
            for d in final[pretype]:
                count+=1
                
                if t>d-5 and t<d+5:
                    # print("yes")
                    trainyear.append(final.index[count])
                    break
        
        #预测
        predata=Data_eco_scaler.loc[Data_eco_scaler["Year"].isin(range(int(PreStartYear),int(PreEndYear)+1))]
        predatatrain=pca.transform(predata[Index].values)
        predict=pca_model.predict(predatatrain)
        #PCA线性模型参数
        #pca_coef = pca_model.coef_
        
        #存储
        ytrain=pca_predict.tolist()
        ypre=np.array(predict).squeeze().tolist()
        
        result={"trainfromyear":trainyear[0],"traintoyear":trainyear[-1],"trainresult":ytrain,"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre,"MAPE":mape,"RMSE":rmse}
        return result 

if __name__ == '__main__':
    StartYear="2010"
    EndYear="2019"
    PreStartYear="2020"
    PreEndYear="2021"
    econamelist=["GDP1","GDP2","GDP"]
    pretype="第一产业用电量"
    city="云南省"
    
    result=PCAindustry(StartYear,EndYear,PreStartYear,PreEndYear,pretype,econamelist,city="云南省")


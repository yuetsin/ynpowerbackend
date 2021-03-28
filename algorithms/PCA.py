# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 12:17:51 2021

@author: ZR_YL
"""

from scipy.stats import pearsonr
from scipy.spatial.distance import pdist, squareform

import algorithms.predict_economic as preeco
from dao.interface import getData
import json 

from sklearn.decomposition import PCA as sklearnPCA

import numpy as np
import pandas as pd
import copy


def PCA(StartYear,EndYear,pretype,econamelist,pmin = 0.9,city="云南省"):

    
    period=int(EndYear)-int(StartYear)+1
    #读取历史负荷数据
    finaldata=[]
    name=[]
    if pretype == None:
        pass
    else:
        for i in range(len(pretype)):
            datajson = getData("云南省_year_电力电量类", pretype[i], StartYear, EndYear)
            data=json.loads(datajson)
            finaldata.append(data)
            name.append(pretype[i])
    
    if econamelist == None:
        pass
    else:
        #读取经济数据
        for i in range(len(econamelist)):
            ecodatajson=getData("云南省_year_社会经济类", econamelist[i], StartYear, EndYear)
            ecodata=json.loads(ecodatajson)
            finaldata.append(ecodata)
            name.append(econamelist[i])

    #获取最终数据DataFrame
    final=pd.DataFrame(finaldata,index=name)
    final=final
    
    data=final.values

    data2 = []
    dmean = []
    dstd = []
    data3 = []
    

    
    
    for i in range(1,len(data)):
        pccs = pearsonr(data[i], data[0])
        if pccs[0] > pmin:
            data2 = np.r_[data2,data[i]]
    
    
    data2 = np.array(data2).reshape(-1,period)

    
    data3 = copy.deepcopy(data2)
    
    for i in range(len(data2)):
        dmean.append(np.mean(data2[i]))
        dstd.append(np.std(data2[i], ddof = 1))
        data3[i] = [(x - dmean[i]) / dstd[i] for x in data2[i]]
        
    
    
    cov = np.cov(data3)
    
    eig_val, eig_vec = np.linalg.eig(cov)
    s = sum(eig_val)
    p = [x / s for x in eig_val]
    
    vector=[]
    variance_ratio=[]
    for i in range(len(p)):
        if p[i]>0.5:
            vector.append(eig_vec[i].tolist())
            variance_ratio.append(p[i])
    n_components=len(variance_ratio)
        
    
    #获取合适的PCA维度
    # pca = sklearnPCA(0.9)
    # principalComponents = pca.fit_transform(data)
    # #print("n_components = ",pca.n_components_)
    # print(pca.explained_variance_ratio_)
    # print(pca.explained_variance_)
    
    return {"N_components":n_components,"ComponetRatio":variance_ratio,"Vectors":vector}

if __name__ == '__main__':
    StartYear="1995"
    EndYear="2015"
    pretype=["全社会用电量"]
    econamelist=["GDP","第一产业GDP","第二产业GDP"]
    
    result=PCA(StartYear,EndYear,pretype,econamelist)
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:17:10 2021

@author: ZR_YL
"""

import numpy as np
import pandas as pd

import algorithms.predict_economic as preeco
from dao.interface import getData
import json 

from sklearn import metrics
from sklearn.cluster import KMeans





def Kmeans(StartYear,EndYear,pretype,econamelist,n_clusters,city="云南省"):
    """
    

    Parameters
    ----------
    StartYear : TYPE
        DESCRIPTION.
    EndYear : TYPE
        DESCRIPTION.
    pretype : list
        DESCRIPTION.
    econamelist : list
        DESCRIPTION.
    n_clusters : int
        簇的个数.
    city : TYPE, optional
        DESCRIPTION. The default is "云南省".

    """
    if n_clusters>len(econamelist):
        return {"FactorsName":"聚类数过大，请重新选取"}
    else:
        finaldata=[]
        name=[]
        if pretype == None:
            pass
        else:
            #读取历史负荷数据
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
        
        estimator = KMeans(n_clusters)
        estimator.fit(final)
        label_pred = estimator.labels_
        centroids = estimator.cluster_centers_ 
        
        relatedlabel=label_pred.tolist()
        relatedname= []
        
        
        for n in range(n_clusters):
            label=[]
            for i in range(len(relatedlabel)):
                if relatedlabel[i] == n:
                    label.append(name[i])
            relatedname.append(label)
            
        
        
        return {"Clusters":relatedname}

if __name__ == '__main__':
    StartYear="1995"
    EndYear="2015"
    pretype=["全社会用电量"]
    econamelist=["GDP","第一产业GDP","第二产业GDP"]
    
    result=Kmeans(StartYear,EndYear,pretype,econamelist,2,city="云南省")

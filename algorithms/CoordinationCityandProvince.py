# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 15:49:16 2021

@author: ZR_YL
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from scipy.optimize import leastsq
import math as m

import algorithms.predict_economic as preeco
from dao.interface import getData
import json 


def CoordinationCityandProvince(File):

    data=pd.read_csv(File)
    year=data.columns[0]
    yeardata=data[year]
    city=data.columns[1:-1]
    allcitydata=data[city].values
    prov=data.columns[-1]
    allprovincedata=data[prov].values
    
    coord=[]
    for i in range(len(yeardata)):
        citydata=allcitydata[i]
        provincedata=allprovincedata[i]
        dz = sum(citydata) - provincedata
        ci2 = [x*x for x in citydata]
        pr2 = provincedata * provincedata/5
        sum2 = sum(ci2) + pr2
        newpr = provincedata + (pr2 / sum2)*dz
        newci=[]
        for i in range(len(citydata)):
            newci.append(citydata[i]-(ci2[i] / sum2)*dz)
        coord.append(newci)
    
    result=pd.DataFrame(coord)
    result.columns=data.columns[1:-1]
    result.insert(0,year,yeardata)

    return result

if __name__=="__main__":
    
    File=r"C:\ZHD\Project\dclab\ynpower\ynpowerbackend\algorithms\云南省各地市预测值.csv"
    result=CoordinationCityandProvince(File)
    print(result)
# result[year]=yeardata
#     return {"cityname":city,"cooresults":newci}
# else:
#     return {"cityname":None,"cooresults":"%s的%s数据缺失，请补充后再运行该程序"%(Cooryear,lossdata)}


# if __name__ == '__main__':
#     Cooryear="2019"
#     pretype="预测用电量"
#     city=CoordinationCityandProvince(Cooryear,pretype)
# def CoordinationCityandProvince(Cooryear,pretype):
#     city = ["保山","楚雄","大理","德宏","迪庆","红河","昆明","丽江","临沧","怒江","普洱","曲靖","文山","西双版纳","玉溪","昭通"]
#     key=0
#     citydata=[]
#     lossdata=[]
#     #读取全省数据
#     pdatajson = getData("yunnan_year_电力电量类", pretype, Cooryear, Cooryear)
#     if isinstance(pdatajson, dict):
#         key+=1
#         print("云南省 的 %s 未存储在数据库中！"%(pretype))
#         lossdata.append("云南省")
#     else:
#         pdata=json.loads(pdatajson)
#         provincedata = pdata[Cooryear]
#     #读取各地市数据
    
#     for c in city:
#         datajson = getData("%s_year_电力电量类"%c, pretype, Cooryear, Cooryear)

#         if isinstance(datajson, dict):
#             key+=1
#             print("%s 的 %s 未存储在数据库中！"%(c,pretype))
#             lossdata.append(c)
#             continue
#         data=json.loads(datajson)
#         citydata.append(data[Cooryear])
#     if key==0:
    
#         dz = sum(citydata) - provincedata
#         ci2 = [x*x for x in citydata]
#         pr2 = provincedata * provincedata/5
#         sum2 = sum(ci2) + pr2
#         newpr = provincedata + (pr2 / sum2)*dz
#         newci=[]
#         for i in range(len(citydata)):
#             newci.append(citydata[i]-(ci2[i] / sum2)*dz)
#         return {"cityname":city,"cooresults":newci}
#     else:
#         return {"cityname":None,"cooresults":"%s的%s数据缺失，请补充后再运行该程序"%(Cooryear,lossdata)}


# if __name__ == '__main__':
#     Cooryear="2019"
#     pretype="预测用电量"
#     city=CoordinationCityandProvince(Cooryear,pretype)
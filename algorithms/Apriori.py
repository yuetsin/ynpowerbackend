# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:46:59 2021

@author: ZR_YL
"""


import algorithms.predict_economic as preeco
from dao.interface import getData
import json 

import numpy as np
import pandas as pd
import copy

def Apriori(StartYear,EndYear,pretype,econamelist,city="云南省"):
    loadlist=None
    def frecount(vnum,data1,data2,f):
        
        fre = np.zeros(shape=(4,4))
    
        for i in range(len(data2)):
            x = data1[i] 
            y = data2[i]
            if x == 4: 
                x = x - 1#最大值4归到第三类
            if y == 4: 
                y = y - 1
            fre[x][y] =  fre[x][y] + 1
    

        fre2 = [x / len(data1) for x in fre]
        # print(fre2)
        
        score=0
        confidence=1
        for i in range(4):
            for k in range(4):
                if fre[i][k] > f :
                    score=score+fre[i][k]/vnum
                    c=fre[i][k]/sum(fre[i])
                    if confidence>c:
                        confidence=c
                    print("负荷等级" +str(i)+"与因素等级"+str(k)+"有关联,支持度为"+str(fre[i][k]/vnum)+"，置信度为"+str(c))
        
        
        return score,confidence
    
    period=int(EndYear)-int(StartYear)+1
    #读取历史负荷数据
    finaldata=[]
    name=[pretype]
    datajson = getData("云南省_year_电力电量类", pretype, StartYear, EndYear)
    data=json.loads(datajson)
    finaldata.append(data)


    if loadlist == None:
        pass
    else:
        for i in range(len(loadlist)):
            datajson = getData("云南省_year_电力电量类", loadlist[i], StartYear, EndYear)
            data=json.loads(datajson)
            finaldata.append(data)
            name.append(loadlist[i])
    
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
    data2 =[]
    
    for i in range(len(final)):
        fg = 0
        m = min(data[i])
        d = max(data[i]) - m
        dd = [ int((x - m) / d * 4 ) for x in data[i]] #归一化
        
        # for k in range(4):
        #     num = str(dd).count(str(k))
        #     if num > (len(data) / 2):
        #         fg = 1
        #         break

        # if fg == 1:#如果分类结果不理想，则重新分类
        #     sor = sorted(data[i])
        #     dd = []
        #     for k in range(len(data.T) - 1):
        #         d = sor.index(data[i][k])
                
        #         dd.append(int(d /(len(final)/4) ))
        
        data2.append(dd)
    
    factorname=[]
    factorconfi=[]
    factorscore=[]    
    
    for i in range(1,len(data)):
        print("分析第"+str(i+1)+"个因素")
        factor=frecount(len(final.T), data2[0],data2[i],4)
        factorname.append(name[i])
        factorconfi.append(factor[1])
        factorscore.append(factor[0])
    return {"FactorsName":factorname,"Score":factorscore,"Confidence":factorconfi}

if __name__ == '__main__':
    StartYear="1995"
    EndYear="2015"
    pretype="全社会用电量"
    econamelist=["人均GDP","能源消费总值","第一产业GDP","第二产业GDP","GDP","人口"]
    
    result=Apriori(StartYear,EndYear,pretype,econamelist)
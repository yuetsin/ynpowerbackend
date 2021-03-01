# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:01:08 2020

@author: ZR_YL
"""


##这个方法效果很差，暂时放弃
import numpy as np
import pandas as pd
from sklearn.svm import SVR
# from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import MultiOutputRegressor
from algorithms.train_test_set import generate_data,inverse_data

from algorithms.evaluation import RMSE,MAPE
from algorithms.interface import getData
import json 
import math


"""SVM，未联调，已修改"""

def SVM(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype="consumption",region="云南省", kind = "电力电量类", grain="year"):
    #读取数据，确定参数
    name=[pretype]
    finaldata=[]
    outputlen=int(PreEndYear)-int(PreStartYear)+1
    
    datajson=getData(region+"_"+grain+"_"+kind, pretype, StartYear, EndYear)
    data=json.loads(datajson)
    finaldata.append(data)
    final=pd.DataFrame(finaldata,index=name)
    final=final.T

    
    test_size=0#测试数据集应当取0才可以
    X,y=generate_data(final,timestep,outputlen,test_size=test_size,if_norm="no")
    testdata=final[pretype].values
    testinput=[]
    testoutput=[]


    X,y=generate_data(final,timestep,outputlen,test_size=test_size,if_norm="no")
    svr=SVR(kernel="poly",gamma="scale",C= 0.1)#kernel="linear","poly"
    multi_model = MultiOutputRegressor(svr)
    multi_model.fit(X["train"],y["train"])


    testdata=final.values
    
    num=len(X["train"])
    selet=int(np.floor(num/2))
    testinput=X["train"][selet:,:]
    testoutput=y["train"][selet:,:]


    y_svr =multi_model.predict(testinput)
    y_svr_real=np.array(y_svr).reshape(-1,1)
    y_real=np.array(testoutput).reshape(-1,1)

    mape=MAPE(y_svr_real,y_real)
    rmse=RMSE(y_svr_real,y_real)


    pre=multi_model.predict(np.array(np.flipud(testdata[-1:-(timestep+1):-1])).reshape(1,-1))

    ytrain=y_svr[-1]
    trainyear=[]
    for t in testoutput[-1]:
        count=-1
        for d in final[pretype]:
            count+=1
            if t>d-1 and t<d+1:
                trainyear.append(final.index[count])
                break

    ypre=np.array(pre).flatten()
    result={"trainfromyear":trainyear[0],"traintoyear":trainyear[-1],"trainresult":list(ytrain),"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":list(ypre),"MAPE":mape,"RMSE":rmse}
    #保存
    return result
if __name__ == '__main__':
    StartYear="1990"
    EndYear="2019"
    PreStartYear="2020"
    PreEndYear="2021"
    timestep=10
    pretype="consumption"
    city="云南省"

    result=SVM(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype,city)








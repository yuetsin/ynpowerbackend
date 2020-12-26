# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:02:19 2020

@author: ZR_YL
"""

import numpy as np
import csv
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import math


scaler=MinMaxScaler(feature_range=(0,1),copy=False)
def rnn_data(data,num_data,num_steps,outputlen,labels=False):
    """example:[1,2,3,4,5],time_steps=2
        if labels=False, [[1,2],[2,3],[3,4]]
        if labels=True, [3,4,5]
    """
    #num_seq=math.floor((num_data-num_steps)/outputlen)
    num_seq=num_data-num_steps-outputlen+1

    if labels:
        X=np.zeros((num_seq,outputlen))
        for i in range(num_seq):                                                               
           X[i]=data[i+num_steps:i+num_steps+outputlen].T
    else:
        X=np.zeros((num_seq,num_steps))
        for i in range(num_seq):
            X[i]=data[i:i+num_steps].T
            #rnn_df.append(data_ if len(data_.shape)>1 else [[i] for i in data_])
    X=np.array(X,dtype=np.float32)
    return X
#np.array(rnn_df)

def split_data(data,test_size=0.1):
    ntest=int(round(len(data)*(1-test_size)))
    #nval=int(round(len(data[ntest:])*(1-val_size)))   
    df_train,df_test=data[0:ntest],data[ntest:]
    return df_train,df_test

def prepare_data(data,num_data,time_steps,outputlen,labels=False,test_size=0.1):
    DATA=rnn_data(data,num_data,time_steps,outputlen,labels)
    df_train,df_test=split_data(DATA,test_size)
    return (df_train,df_test)
'''def prepare_data(data,time_steps,labels=False,val_size=0.1,test_size=0.1):
    DATA=rnn_data(data,time_steps,labels)
    df_train,df_val,df_test=split_data(DATA,val_size,test_size)
    return (df_train,df_val,df_test)'''

'''读取数据库的数据时用这个'''
# def generate_data(File,columns,num_steps,outputlen,labels=False,test_size=0.1):
#     #consumption=pd.read_csv(File)
#     consumption=File
#     l=consumption.columns
#     print(l)
#     num_data=len(consumption[l[columns]].values)
#     consumption=consumption[l[columns]].values
#     consumption=np.array(consumption,dtype=np.float32)
#     consumption=consumption.reshape(-1,1)
#     consumption=scaler.fit_transform(consumption)
#     train_x, test_x = prepare_data(consumption, num_data=num_data,time_steps=num_steps,outputlen=outputlen,test_size=test_size)
#     train_y, test_y = prepare_data(consumption, num_data=num_data, time_steps=num_steps,outputlen=outputlen,test_size=test_size,labels=True)
#     return dict(train=train_x,test=test_x), dict(train=train_y,test=test_y)

def generate_data(consumption,num_steps,outputlen,labels=False,test_size=0.1,if_norm="yes"):
    column=consumption.columns
    num_data=len(consumption[column[0]].values)
    consumption=consumption[column[0]].values
    consumption=np.array(consumption,dtype=np.float32)
    consumption=consumption.reshape(-1,1)
    if if_norm=="yes":
        consumption=scaler.fit_transform(consumption)
    else:
        consumption=consumption
    train_x, test_x = prepare_data(consumption, num_data=num_data,time_steps=num_steps,outputlen=outputlen,test_size=test_size)
    train_y, test_y = prepare_data(consumption, num_data=num_data, time_steps=num_steps,outputlen=outputlen,test_size=test_size,labels=True)
    return dict(train=train_x,test=test_x), dict(train=train_y,test=test_y)

def inverse_data(data):
    return scaler.inverse_transform(data)

def norm(data):
    return scaler.fit_transform(data)


# File="D:/lab/Yunnan_Pre/data/load_data/yunnan_year_load.csv"
# Data=pd.read_csv(File)
# X,Y=generate_data(File,4,2,test_size=0.3)
# Y_real=inverse_data(Y["test"])
    
# from interface import getData
# import json 

# resultJson = getData("yunnan_year", "load", "2008", "2016")
# data=json.loads(resultJson)
# File=pd.DataFrame.from_dict(data,orient = 'index',columns=["load"])
# timestep=3#
# outputlen=1#预测年限
# X1,y1=generate_data(File,0,timestep,outputlen)
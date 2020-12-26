# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 12:57:30 2020

@author: ZR_YL
"""



import numpy as np
import pandas as pd

#评价指标

def RMSE(y_pre,y_test):
    
    y_pre=np.array(y_pre).reshape(-1,1)
    y_test=np.array(y_test).reshape(-1,1)
    num=len(y_test)
    mae2=np.sum(np.square(y_pre-y_test))
    rmse=np.sqrt(mae2/num)
    return rmse

def MAPE(y_pre,y_test):
    y_pre=np.array(y_pre).reshape(-1,1)
    y_test=np.array(y_test).reshape(-1,1)
    return np.mean(np.abs((y_pre - y_test) / y_test)) * 100


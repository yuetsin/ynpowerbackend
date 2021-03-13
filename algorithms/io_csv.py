"""从csv文件中读写数据"""

import numpy as np
import pandas as pd
import random
import math





"""生成概率预测值"""
def getpred(x,year,planflag,plan):
    #求各个指标的增长率
    gr = []
    for i in range(len(x) - 1):
        gr.append(x[i+1] / x[i] - 1)
    std = np.std(gr,ddof=1)
    
    if np.isnan(std):
        std=0.000000001
    
    if planflag == 1:
        m = plan / 100
        
    elif planflag == 0:
        m = np.mean(gr)
    

    xdata = []

    for i in range(year*51):
        xdata.append(random.normalvariate(m, std))
    xdata = np.array(xdata).reshape(year,51)

    xdata = [x + 1 for x in xdata]
    xdata2 = xdata[:]

    for i in range(51):
        for j in range(year):
            if j !=0:
                xdata2[j][i] = xdata2[j][i] * xdata2[j - 1][i]

                
    return xdata2

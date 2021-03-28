# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 13:42:44 2020

@author: ZR_YL
"""


import pandas as pd
import csv
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import algorithms.predict_economic as predict

from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json 

"""模糊线性回归,FLR"""


def FLR(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype="全社会用电量",city="云南省"):
    """
    

    Parameters
    ----------
    StartYear : TYPE
        DESCRIPTION.
    EndYear : TYPE
        DESCRIPTION.
    PreStartYear : TYPE
        DESCRIPTION.
    PreEndYear : TYPE
        DESCRIPTION.
    timestep : TYPE
        DESCRIPTION.
    pretype : TYPE, optional
        DESCRIPTION. The default is "consumption".
    city : TYPE, optional
        DESCRIPTION. The default is "云南省".

    Returns
    -------
    None.

    """
    if timestep > (int(EndYear)-int(StartYear)+1):
        return {"trainfromyear":None,"traintoyear":None,"trainresult":None,"prefromyear":None,"pretoyear":None,"preresult":"训练步长过大，请调整后重试.","MAPE":None,"RMSE":None}
    else:

        #读取数据
        datajson=getData("云南省_year_电力电量类", pretype, StartYear, EndYear)
        data=json.loads(datajson)
        
        name=[pretype]
        finaldata=[]
        finaldata.append(data)
        final=pd.DataFrame(finaldata,index=name)
    
        period=int(PreEndYear)-int(PreStartYear)+1
    
        econamelist=["第一产业GDP","第二产业GDP","第三产业GDP"]
        #读取经济数据
        for i in range(len(econamelist)):
            
            ecodatajson=getData("云南省_year_社会经济类", econamelist[i], StartYear, EndYear)
            ecodata=json.loads(ecodatajson)
            finaldata.append(ecodata)
            name.append(econamelist[i])
            #获取最终数据DataFrame
        final=pd.DataFrame(finaldata,index=name)
        final=final.T
        #获取训练所用的数据集
        data1=final.iloc[len(final.values)-timestep:]
        num=len(data1.values)
        
        #预测经济数据
        eco=predict.pre(data1,econamelist[0],PreStartYear,PreEndYear)
        for j in range(1,len(econamelist)):
            c=predict.pre(data1,econamelist[j],PreStartYear,PreEndYear)
            eco=pd.merge(eco,c,on="year")  
    
        #获得训练集和测试集
        trainx=eco.loc[:,econamelist]
        trainy=data1.loc[:,pretype]
        prex=eco.loc[num:,econamelist]
    
        #创建模糊控制变量
        
        GDP1=ctrl.Antecedent(np.arange( 100, 15000, 20 ), "gdp1" )
        GDP2=ctrl.Antecedent(np.arange( 150, 20000, 20 ), "gdp2" )
        # GDP3=ctrl.Antecedent(np.arange( 100, 25000, 20 ), "gdp3" )
        fuload=ctrl.Consequent(np.arange( 100, 8000, 1 ), "futureload" )
        
        #定义模糊集和其隶属度函数
        
        GDP1[ "very low" ] = fuzz.trimf( GDP1.universe, [ 100, 300, 500 ] )
        GDP1[ "low" ] = fuzz.trimf( GDP1.universe, [ 400, 850, 1250 ] )
        GDP1[ "medium" ] = fuzz.trimf( GDP1.universe, [ 1000, 2500, 4000 ] )
        GDP1[ "high" ] = fuzz.trimf( GDP1.universe, [ 3700, 5500, 7500] )
        GDP1[ "very high" ] = fuzz.trimf( GDP1.universe, [ 7300, 12000, 15000] )
        
        GDP2[ "very low" ] = fuzz.trimf(GDP2.universe, [ 100, 500, 900 ] )
        GDP2[ "low" ] = fuzz.trimf(GDP2.universe, [ 500, 1450, 2600 ] )
        GDP2[ "medium" ] = fuzz.trimf(GDP2.universe, [ 2500, 6500, 10500 ] )
        GDP2[ "high" ] = fuzz.trimf(GDP2.universe, [ 9500, 12000, 14000] )
        GDP2[ "very high" ] = fuzz.trimf(GDP2.universe, [ 13500, 16000, 20000] )
        
        # GDP3[ "very low" ] = fuzz.trimf(GDP3.universe, [ 100, 400, 700 ] )
        # GDP3[ "low" ] = fuzz.trimf(GDP3.universe, [ 650, 1400, 2750 ] )
        # GDP3[ "medium" ] = fuzz.trimf(GDP3.universe, [ 2600, 6000, 13000 ] )
        # GDP3[ "high" ] = fuzz.trimf(GDP3.universe, [ 12000, 15000, 18000] )
        # GDP3[ "very high" ] = fuzz.trimf(GDP3.universe, [ 17000, 21000, 25000] )
        
        fuload[ "very low" ] = fuzz.trimf( fuload.universe, [ 100, 200, 300 ] )
        fuload[ "low" ] = fuzz.trimf( fuload.universe, [ 250, 550, 1100 ] )
        fuload[ "medium" ] = fuzz.trimf( fuload.universe, [ 1050, 1900, 3000 ] )
        fuload[ "high" ] = fuzz.trimf( fuload.universe, [ 2750, 3500, 5100 ] )
        fuload[ "very high" ] = fuzz.trimf(fuload.universe, [ 5000, 8000, 8000 ] )
        
        # #定义模糊规则
        rule=locals()
        rule1 = ctrl.Rule(GDP1[ "very low" ]&GDP2[ "very low" ], fuload[ "very low" ] )
        rule2 = ctrl.Rule(GDP1[ "very low" ]&GDP2[ "low" ], fuload[ "very low" ] )
        rule3 = ctrl.Rule(GDP1[ "very low" ]&GDP2[ "medium" ], fuload[ "low" ] )
        rule4 = ctrl.Rule(GDP1[ "very low" ]&GDP2[ "high"  ], fuload[ "medium" ] )
        rule5 = ctrl.Rule(GDP1[ "very low" ]&GDP2[ "very high" ], fuload[ "medium" ] )
        
        rule6 = ctrl.Rule(GDP1[ "low" ]&GDP2[ "very low" ], fuload["very low" ] )
        rule7 = ctrl.Rule(GDP1[ "low" ]&GDP2[ "low" ], fuload[ "low"  ] )
        rule8 = ctrl.Rule(GDP1[ "low" ]&GDP2[ "medium" ], fuload[ "low"  ]  )
        rule9 = ctrl.Rule(GDP1[ "low" ]&GDP2[ "high"  ], fuload["medium" ]  )
        rule10 = ctrl.Rule(GDP1[ "low" ]&GDP2[ "very high"  ], fuload["medium" ] )
        
        rule11 = ctrl.Rule(GDP1[ "medium" ]&GDP2[ "very low" ], fuload["low" ] )
        rule12 = ctrl.Rule(GDP1[ "medium" ]&GDP2[ "low"  ], fuload["low" ] )
        rule13 = ctrl.Rule(GDP1[ "medium" ]&GDP2[ "medium" ], fuload["medium" ] )
        rule14 = ctrl.Rule(GDP1[  "medium" ]&GDP2[ "high"  ], fuload["high" ] )
        rule15 = ctrl.Rule(GDP1[  "medium" ]&GDP2[ "very high" ], fuload["medium" ] )
        
        rule16 = ctrl.Rule(GDP1[ "high" ]&GDP2[ "very low" ], fuload["low" ] )
        rule17 = ctrl.Rule(GDP1[ "high" ]&GDP2[ "low"  ], fuload["medium" ] )
        rule18 = ctrl.Rule(GDP1[ "high" ]&GDP2[ "medium" ], fuload["high"] )
        rule19 = ctrl.Rule(GDP1[  "high" ]&GDP2[ "high"  ], fuload["high" ] )
        rule20 = ctrl.Rule(GDP1[  "high" ]&GDP2[ "very high" ], fuload["very high" ] )
        
        rule21 = ctrl.Rule(GDP1[ "very high" ]&GDP2[ "very low" ], fuload["low" ] )
        rule22 = ctrl.Rule(GDP1[ "very high" ]&GDP2[ "low"  ], fuload["low"  ] )
        rule23 = ctrl.Rule(GDP1[ "very high" ]&GDP2[ "medium" ], fuload["medium" ] )
        rule24 = ctrl.Rule(GDP1[  "very high" ]&GDP2[ "high"  ], fuload["high" ] )
        rule25 = ctrl.Rule(GDP1[  "very high" ]&GDP2[ "very high" ], fuload["very high" ] )
        fuzzy_ctrl = ctrl.ControlSystem([ rule1, rule2, rule3, rule4, rule5,rule6, rule7, rule8, rule9, rule10,
                                     rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
                                     rule21, rule22, rule23, rule24, rule25])
    
        consumptionSystem = ctrl.ControlSystemSimulation( fuzzy_ctrl )
    
        #评估
        trainn=len(trainx)
    
    
        systemoutput=np.zeros(trainn, dtype=np.float64 )
        
        for i in range(trainn):
            
            consumptionSystem.input["gdp1"] = trainx.loc[i,econamelist[0]]
            consumptionSystem.input["gdp2"] = trainx.loc[i,econamelist[1]]
            consumptionSystem.compute()
            systemoutput[i] = consumptionSystem.output["futureload"]
    
    
    
        mape=MAPE(systemoutput[num-period:num],trainy.values[num-period:num])
        rmse=RMSE(systemoutput[num-period:num],trainy.values[num-period:num])
    
        
        #保存结果
    
        trainyear=data1.index
        ytrain=np.array(systemoutput[:num]).reshape(1,-1).squeeze()
        ypre=np.array(systemoutput[num:]).reshape(1,-1).squeeze()
    
        result={"trainfromyear":trainyear[0],"traintoyear":trainyear[-1],"trainresult":ytrain.tolist(),"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre.tolist(),"MAPE":mape,"RMSE":rmse}
    
        return result

if __name__=="__main__":
    StartYear="1990"
    EndYear="2019"
    PreStartYear="2020"
    PreEndYear="2029"
    timestep=15
    result=FLR(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype="全社会用电量",city="云南省")
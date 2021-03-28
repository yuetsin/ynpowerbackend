# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 12:09:48 2020

@author: ZR_YL
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import math
from algorithms.train_test_set import generate_data,inverse_data

from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json 



"""BPNN，已修改"""

def BPNN(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype="全社会用电量",city="云南省", hidden=[24,12], learningrate=0.005,epoch=1000):
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
    hidden : TYPE, optional
        神经网络的隐藏层, list, 几个元素代表几层，每层神经元个数为list元素值. The default is [24,12].
    learningrate : TYPE, optional
        神经网络学习率. The default is 0.005.
    epoch : TYPE, optional
        训练学习次数. The default is 1000.

    Returns
    -------
    None.

    """
    
    def bpnn(timestep,outputlen,x_train,y_train,x_test,y_test,x_pre,hiddenneron,lr,epoch):
        x=tf.placeholder(tf.float32,shape=[None,timestep],name="Input")
        y=tf.placeholder(tf.float32,shape=[None,outputlen],name="Onput")
        hlen=len(hiddenneron)
        f=locals()
        for i in range(hlen+1):
            if i==0:
                f["f%s"%(i+1)]=tf.contrib.layers.fully_connected (x,hiddenneron[i])
            else:
                if i== hlen:
                    pre=tf.contrib.layers.fully_connected (f["f%s"%(i)],outputlen)
                else:
                    f["f%s"%(i+1)]=tf.contrib.layers.fully_connected (f["f%s"%(i)],hiddenneron[i])
        
        loss=tf.losses.mean_squared_error(y, pre)
    
        train_op = tf.train.AdamOptimizer(lr).minimize(loss)
        
        saver = tf.train.Saver()
        
        with tf.Session() as sess:
            init=tf.initialize_all_variables()
            sess.run(init)
            for i in range(epoch):
                sess.run(train_op,feed_dict={x:x_train,y:y_train})
                lossz=sess.run(loss,feed_dict={x:x_train,y:y_train})
                if i%50==0:
                    print(lossz)
            
            y_train_pre=sess.run(pre,feed_dict={x:x_train}) 
            
            y_test_pre=sess.run(pre,feed_dict={x:x_test}) 
            
            y_pre=sess.run(pre,feed_dict={x:x_pre}) 
            
            training=np.array(y_train_pre).squeeze()
            
            predictions=np.array(y_test_pre).squeeze()
            labels=np.array(y_test).squeeze()
            # saver.save(sess, "D:/lab/Yunnan_Pre/result/yunnan_shortterm_钢铁_BPNN/")
        return predictions,labels,y_pre,training


    #读取数据，确定参数
    name=[pretype]
    finaldata=[]
    outputlen=int(PreEndYear)-int(PreStartYear)+1
    
    datajson=getData("云南省_year_电力电量类", pretype, StartYear, EndYear)
    data=json.loads(datajson)
    finaldata.append(data)
    final=pd.DataFrame(finaldata,index=name)
    final=final.T

    
    test_size=0#测试数据集应当取0才可以
    X,y=generate_data(final,timestep,outputlen,test_size=test_size,if_norm="no")
    testdata=final[pretype].values
    testinput=[]
    testoutput=[]
    
    num=len(X["train"])
    selet=int(np.floor(num/2))
    testinput=X["train"][selet:,:]
    testoutput=y["train"][selet:,:]
    
    x_pre=np.array(np.flipud(testdata[-1:-(timestep+1):-1])).reshape(1,-1)
    
    test_pre,test_label,pre,training=bpnn(timestep,outputlen,X["train"][:-1,:],y["train"][:-1,:],testinput,testoutput,x_pre,hidden,learningrate,epoch)
    
    mape=MAPE(test_pre,test_label)
    rmse=RMSE(test_pre,test_label)
    
    
    #保存训练结果,年份上可能有问题
    #trainingtrue=y["train"][:-1,:].flatten()
    trainingtrue=y["train"][-1,:]
    
    trainyear=[]
    for t in trainingtrue:
        count=-1
        for d in final[pretype]:
            count+=1
            
            if t>d-5 and t<d+5:
                # print("yes")
                trainyear.append(final.index[count])
                break
    
    ytrain=training[-1].tolist()
    ypre=pre.flatten().tolist()
    
    #trainsave.to_csv("D:/lab/Yunnan_Pre/result/yunnan_shortterm_consumption_BPNN_training.csv")
    result={"trainfromyear":trainyear[0],"traintoyear":trainyear[-1],"trainresult":ytrain,"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre,"MAPE":mape,"RMSE":rmse}
    #保存
    return result

if __name__ == '__main__':
    StartYear="1990"
    EndYear="2019"
    PreStartYear="2020"
    PreEndYear="2021"
    timestep=10
    pretype="全社会用电量"
    city="云南省"
    
    result=BPNN(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype,city, hidden=[24,12], learningrate=0.005,epoch=1000)









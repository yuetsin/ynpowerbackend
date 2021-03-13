# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:04:06 2021

@author: ZR_YL
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 10:17:01 2021

@author: ZR_YL
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import math
from algorithms.train_test_set import generate_data,inverse_data
import tensorflow as tf
from algorithms.evaluation import RMSE,MAPE
from dao.interface import getData
import json 


"""RNN，未联调，已修改"""
"""不支持组合预测"""
def RNNpre(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype="consumption",city="云南省", hidden_size=24,hidden_layer=1, learningrate=0.005,epoch=1000):

    #搭建LSTM模块
    def RNN(x,y,outputlen,is_training,hidden_size,num_layers,lr,optimizer,keep_pro):
        cell=tf.nn.rnn_cell.BasicRNNCell
        if is_training and keep_pro<1:
            lstmcell=tf.nn.rnn_cell.MultiRNNCell([tf.nn.rnn_cell.DropoutWrapper(cell(hidden_size,activation=tf.nn.softsign),output_keep_prob=keep_pro) for _ in range(num_layers)])
        else:
            lstmcell=tf.nn.rnn_cell.MultiRNNCell([cell(hidden_size) for _ in range(num_layers)])
        x=tf.expand_dims(x,axis=2)
        outputs,current_state=tf.nn.dynamic_rnn(lstmcell,x,dtype=tf.float32)
        output=outputs[:,-1,:]
        predictions=tf.contrib.layers.fully_connected(output,outputlen)
        
        if not is_training:
            return predictions,None,None
        loss=tf.losses.absolute_difference(labels=y,predictions=predictions)
        train_op=tf.contrib.layers.optimize_loss(loss,tf.train.get_global_step(),optimizer=optimizer,learning_rate=lr)
        return predictions,loss,train_op
    
    #训练模型模块
    def trainmodel(sess,outputlen,train_x,train_y,hidden_size,num_layers,lr,optimizer,keep_pro,batch_size,training_step):
        ds=tf.data.Dataset.from_tensor_slices((train_x,train_y))
        ds=ds.repeat().shuffle(100).batch(batch_size)
        x,y=ds.make_one_shot_iterator().get_next()
        prediction,loss,train_op=RNN(x,y,outputlen,True,hidden_size,num_layers,lr,optimizer,keep_pro)
        losses=[]
        sess.run(tf.global_variables_initializer())
        ytrain=[]
        for j in range(training_step):
            y,p,l=sess.run([prediction,train_op,loss])
            ytrain.append(y)
        return ytrain
    
    
    #测试模型模块    
    def runmodel(sess,outputlen,test_x,test_y,hidden_size,num_layers,lr,optimizer,keep_pro,batch_size,training_step):
        ds=tf.data.Dataset.from_tensor_slices((test_x,test_y))
        ds=ds.batch(1)
        x,y=ds.make_one_shot_iterator().get_next()
        prediction,_,_=RNN(x,[0.0],outputlen,False,hidden_size,num_layers,lr,optimizer,keep_pro)
        pre=[]
        label=[]
        for j in range(len(test_y)):

            p,l=sess.run([prediction,y])
            pre.append(p)
            label.append(l)

        pre=np.array(pre).squeeze()
        labels=np.array(label).squeeze()


        return pre,labels
    
        #预测模型模块    
    def premodel(sess,outputlen,test_x,test_y,hidden_size,num_layers,lr,optimizer,keep_pro,batch_size,training_step):

        prediction,_,_=RNN(test_x,[0.0],outputlen,False,hidden_size,num_layers,lr,optimizer,keep_pro)
        finalpre=sess.run(prediction)
        return finalpre


    #设置参数

    optimizer="Adam"
    keep_pro=0.9
    batch_size=16

    
    #读取数据，确定参数
    name=[pretype]
    finaldata=[]
    outputlen=int(PreEndYear)-int(PreStartYear)+1
    
    datajson=getData("yunnan_year_电力电量类", pretype, StartYear, EndYear)
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
    
    #最终预测需要的数据
    x_pre=testdata[-1:-(timestep+1):-1].reshape(1,-1)
    x_pre=np.array(x_pre, dtype = np.float32)

    #训练模型并预测结果
    tf.reset_default_graph()
    with tf.Session() as sess:
        
        with tf.variable_scope("LSTM"):
            ytrain=trainmodel(sess,outputlen,X["train"][:-1,:],y["train"][:-1,:],hidden_size,hidden_layer,learningrate,optimizer,keep_pro,batch_size,epoch)
            
        with tf.variable_scope("LSTM",reuse=True):
            test_pre,test_label=runmodel(sess,outputlen,testinput,testoutput,hidden_size,hidden_layer,learningrate,optimizer,keep_pro,batch_size,epoch)
        with tf.variable_scope("LSTM",reuse=True):   
            ypre=premodel(sess,outputlen,x_pre,x_pre,hidden_size,hidden_layer,learningrate,optimizer,keep_pro,batch_size,epoch)
    
    mape=MAPE(test_pre,test_label)
    rmse=RMSE(test_pre,test_label)
    
    trainyear=[]
    trainingtrue=y["train"][-1,:]
    for t in trainingtrue:
        count=-1
        for d in final[pretype]:
            count+=1
            
            if t>d-5 and t<d+5:
                # print("yes")
                trainyear.append(final.index[count])
                break
    
    result={"prefromyear":PreStartYear,"pretoyear":PreEndYear,"preresult":ypre.tolist()[0],"MAPE":mape,"RMSE":rmse}

    
    return result

StartYear="1990"
EndYear="2019"
PreStartYear="2020"
PreEndYear="2021"
timestep=10
pretype="consumption"
city="云南省"

result=RNNpre(StartYear,EndYear,PreStartYear,PreEndYear,timestep,pretype)
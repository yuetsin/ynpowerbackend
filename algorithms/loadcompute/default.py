import sys
import json
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from algorithms.loadcompute.algorithm import algorithm1

def default_value(key,file,start,end):
	data = algorithm1(key,file,start,end)
	data = json.loads(data)
	x, y = [], []
	for i in range(int(start),int(end)+1):
		x.append(i)
		y.append(data[str(i)])
	x = np.array(x).reshape((-1,1))
	y = np.array(y)
	model = LinearRegression()
	model.fit(x, y)
	x_test = np.array(int(end)+1).reshape((1,-1))
	y_pred = model.predict(x_test)
	return y_pred[0]

def default_souku(file,start,end):
	load_max = default_value("loadmax",file,start,end)
	electricity = default_value("electricity",file,start,end)
	gamma = default_value("gamma",file,start,end)
	beta = default_value("beta",file,start,end)
	return load_max, electricity, gamma, beta

def default_jiabi(file,start,end):
	load_max = default_value("loadmax",file,start,end)
	electricity = default_value("electricity",file,start,end)
	return load_max, electricity

def default_f(file,start,end):
	load_max = default_value("loadmax",file,start,end)
	electricity = default_value("electricity",file,start,end)
	return load_max, electricity

start = "2013"
end = "2018"
# 3个页面均采用文件名为souku结尾的即可
file = "yunnan_year_loadchara-fengshui-souku-max"

loadmax, electricity = default_jiabi(file,start,end)
loadmax, electricity = default_f(file,start,end)
load_max, electricity, gamma, beta = default_souku(file,start,end)
print(load_max, electricity, gamma, beta)
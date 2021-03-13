from dao.interface import getData
import sys
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

def algorithm1(data,file,start,end):
    resultJson = getData(file, data, start,end)
    return resultJson

def pro_data(file,start,end):
    l = ['N00_00', 'N00_15', 'N00_30', 'N00_45', 'N01_00', 'N01_15', 'N01_30',
    'N01_45', 'N02_00', 'N02_15', 'N02_30', 'N02_45', 'N03_00', 'N03_15', 'N03_30',
    'N03_45', 'N04_00', 'N04_15', 'N04_30', 'N04_45', 'N05_00', 'N05_15', 'N05_30',
    'N05_45', 'N06_00', 'N06_15', 'N06_30', 'N06_45', 'N07_00', 'N07_15', 'N07_30',
    'N07_45', 'N08_00', 'N08_15', 'N08_30', 'N08_45', 'N09_00', 'N09_15', 'N09_30',
    'N09_45', 'N10_00', 'N10_15', 'N10_30', 'N10_45', 'N11_00', 'N11_15', 'N11_30',
    'N11_45', 'N12_00', 'N12_15', 'N12_30', 'N12_45', 'N13_00', 'N13_15', 'N13_30',
    'N13_45', 'N14_00', 'N14_15', 'N14_30', 'N14_45', 'N15_00', 'N15_15', 'N15_30',
    'N15_45', 'N16_00', 'N16_15', 'N16_30', 'N16_45', 'N17_00', 'N17_15', 'N17_30',
    'N17_45', 'N18_00', 'N18_15', 'N18_30', 'N18_45', 'N19_00', 'N19_15', 'N19_30',
    'N19_45', 'N20_00', 'N20_15', 'N20_30', 'N20_45', 'N21_00', 'N21_15', 'N21_30',
    'N21_45', 'N22_00', 'N22_15', 'N22_30', 'N22_45', 'N23_00', 'N23_15', 'N23_30',
    'N23_45']
    query = l[0]
    for i in range(1,96):
    	query = query + ','+ l[i]

    result = algorithm1(query,file,start,end)
    data = []
    for i in range(0,96,4):
    	data.append(get_hdata(result,l[i])+get_hdata(result,l[i+1])+get_hdata(result,l[i+2])+
    		get_hdata(result,l[i+3]))
    data = np.hstack(data)
    time = get_time(result,l[0])
    return data, time

def get_mdata(time,data,m):
    # get data of a chosen month
    nrow = time.shape[0]
    index = []
    for i in range(nrow):
        dd = datetime.datetime.strptime(time[i,0], "%Y/%m/%d")
        if dd.month == m:
        	index.append(i)
    m_data = data[index,:]
    return m_data

def get_mtime(time,data,m):
    # get index of a chosen month
    nrow = time.shape[0]
    index = []
    for i in range(nrow):
        dd = datetime.datetime.strptime(time[i,0], "%Y/%m/%d")
        if dd.month == m:
        	index.append(i)
    return index

def get_hdata(data,colname):
	# set resolution to hour
	number = len(data)
	result = []
	for i in range(number):
		if data[i][1] == colname:
			temp = [data[i][2]]
			result.append(temp)
	result = np.array(result)
	return result

def get_time(data,colname):
	# time of all data
	number = len(data)
	result = []
	for i in range(number):
		if data[i][1] == colname:
			temp = [data[i][0]]
			result.append(temp)
	result = np.array(result)
	return result

def character(data):
    max_l = np.max(data)
    # max load 
    min_l = np.min(data)
    #average load
    mean_l = np.mean(data)
    nrow = data.shape[0]
    p2v,ratio = [],[]
    for i in range(nrow):
    	diff = (np.max(data[i,:])-np.min(data[i,:]))/np.max(data[i,:])
    	dive = np.mean(data[i,:])/np.max(data[i,:])
    	p2v.append(diff)
    	ratio.append(dive)

    max_p2v = np.max(np.array(p2v))
    #index = np.where(np.array(p2v)==max_p2v)[0][0]
    #print(np.max(data[index,:]),np.min(data[index,:]))
    y_ratio = np.mean(np.array(ratio))
    return max_l,min_l,mean_l,max_p2v,y_ratio

def m_character(mdata):
	m_max = np.max(mdata)
	m_mean = np.min(mdata)
	m_min = np.mean(mdata)
	d_max_id = np.where(mdata==np.max(mdata))[0][0]
	max_mean = np.mean(mdata[d_max_id,:])
	return m_max, m_mean, m_min, max_mean

def unbalance(time,data,max_l):
	max_t, mean_t, max_mean_t = 0, 0, 0
	for i in range(1,13):
		m_data = get_mdata(time,data,i)
		m_max, m_mean, m_min, max_mean = m_character(m_data)
		max_t += m_max
		mean_t += m_mean
		max_mean_t += max_mean
	s_unbalance = max_t/(12*max_l)
	m_unbalance = mean_t/max_mean_t
	return s_unbalance, m_unbalance

def y_pre_character(data, time):
	max_l,min_l,mean_l,max_p2v,y_ratio = character(data)
	s_unbalance, m_unbalance = unbalance(time,data,max_l)
	return max_l,min_l,mean_l,max_p2v,y_ratio, s_unbalance, m_unbalance

def y_character(file,start,end):
	data = pro_data(file, start,end)[0]
	max_l,min_l,mean_l,max_p2v,y_ratio = character(data)
	time = pro_data(file, start,end)[1]
	s_unbalance, m_unbalance = unbalance(time,data,max_l)
	return max_l,min_l,mean_l,max_p2v,y_ratio, s_unbalance, m_unbalance

def multi_y_character(file,start,end):
	data = pro_data(file, start,end)[0]
	time = pro_data(file, start,end)[1]
	days = time.shape[0]
	years = []
	for i in range(days):
		dd = datetime.datetime.strptime(time[i,0], "%Y/%m/%d")
		years.append(dd.year)
	new_years = list(set(years))
	new_years.sort(key=years.index)
	num_year = len(new_years)

	index_list = [[] for i in range(num_year)]
	for m in range(num_year):
		for d in range(days):
			dd = datetime.datetime.strptime(time[d,0], "%Y/%m/%d")
			if dd.year == new_years[m]:
				index_list[m].append(d)
	data_list = []
	result = []
	for i in range(num_year):
		data_list.append(data[index_list[i],:])
		year_data = data[index_list[i],:]
		year_time = time[index_list[i],:]
		result.append(list(y_pre_character(year_data, year_time)))
	return new_years, result

def typical_day(file,start,end,m):
	data = pro_data(file, start,end)[0]
	time = pro_data(file, start,end)[1]
	if m == 0:
		temp = np.vstack((get_mdata(time,data,3),get_mdata(time,data,4)))
		date = get_mtime(time,data,3)+get_mtime(time,data,4)
	elif m == 1:
		temp = np.vstack((get_mdata(time,data,8),get_mdata(time,data,9)))
		date = get_mtime(time,data,8)+get_mtime(time,data,9)
	elif m == 2:
		temp = get_mdata(time,data,12)
		date = get_mtime(time,data,12)
	else:
		pass
	index_max = date[np.where(temp==np.max(temp))[0][0]]
	index_min = date[np.where(temp==np.min(temp))[0][0]]
	median = np.median(temp)
	dist = np.square(temp-median)
	index_median = date[np.where(dist==np.min(dist))[0][0]]

	return time[index_max,0], time[index_min,0], time[index_median,0], data[index_max,:], data[index_min,:], data[index_median,:]

def y_load(file,start,end):
	data = pro_data(file, start,end)[0]
	time = pro_data(file, start,end)[1]
	max_load = []
	for i in range(1,13):
		m_data = get_mdata(time,data,i)
		m_max = m_character(m_data)[0]
		max_load.append(m_max)
	fig = plt.figure()
	plt.plot(max_load)
	plt.show()

def y_load_cons(file,start,end):
	data = pro_data(file, start,end)[0]
	data = data.reshape((1,-1)).flatten()
	data = -np.sort(-data)
	x = range(1,len(data)+1,1)

	fig = plt.figure()
	plt.plot(x,data)
	plt.show()

if __name__ == '__main__':
	max_l,min_l,mean_l,max_p2v,y_ratio, s_unbalance, m_unbalance = y_character("yunnan_day_电力电量类", 
		"2013/1/1","2013/12/31")
	#print(max_l,min_l,mean_l,max_p2v,y_ratio, s_unbalance, m_unbalance)
	#print(typical_day("yunnan_day_电力电量类","2013/1/1","2013/12/31",0))
	#y_load("yunnan_day_电力电量类","2013/1/1","2013/12/31")
	#y_load_cons("yunnan_day_电力电量类","2013/1/1","2013/12/31")
	
	years, result = multi_y_character("yunnan_day_电力电量类", "2013/1/1","2014/12/31")
	print(result)
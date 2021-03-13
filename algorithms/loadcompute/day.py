import numpy as np
import datetime
import matplotlib.pyplot as plt
from algorithms.loadcompute.algorithm import pro_data

def d_pre_character(data):
	# data shape: np array (24,)
	d_max = np.max(data)
	d_mean = np.mean(data)
	d_min = np.min(data)

	d_r = d_mean/d_max
	d_m_r = d_min/d_max
	peak = d_max - d_min
	peak_r = peak/d_max
	return d_max, d_mean, d_min, d_r, d_m_r, peak, peak_r

def d_character(file,start,end):
	data = pro_data(file,start,end)[0]
	d_max = np.max(data)
	d_mean = np.mean(data)
	d_min = np.min(data)

	d_r = d_mean/d_max
	d_m_r = d_min/d_max
	peak = d_max - d_min
	peak_r = peak/d_max
	return d_max, d_mean, d_min, d_r, d_m_r, peak, peak_r

def multi_d_character(file,start,end):
	data = pro_data(file,start,end)[0]
	time = pro_data(file,start,end)[1]
	days = time.shape[0]
	result = []
	for i in range(days):
		result.append(list(d_pre_character(data[i,:])))
	result = np.array(result)
	return time, result

def day_plot(file,start,end):
	data = pro_data(file,start,end)[0].flatten()
	# fig = plt.figure()
	# plt.plot(data)
	# plt.show()
	return data

if __name__ == '__main__':
	data = pro_data("yunnan_day_电力电量类", "2013/1/1","2013/1/3")[0]
	print(data.shape)
	time = pro_data("yunnan_day_电力电量类", "2013/1/1","2013/1/3")[1]
	print(time)
	t, r = multi_d_character("yunnan_day_电力电量类", "2013/1/1","2013/1/3")
	print(t)
	print(r)
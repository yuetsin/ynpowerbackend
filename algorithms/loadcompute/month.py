import numpy as np
import datetime
import datetime
from algorithms.loadcompute.algorithm import pro_data

def d_character(data):
	d_max = np.max(data)
	d_mean = np.mean(data)
	d_min = np.min(data)

	d_r = d_mean/d_max
	d_min_r = d_min/d_max
	peak = d_max - d_min
	peak_r = peak/d_max
	return d_mean, peak, d_r, d_min_r, peak_r

def m_pre_character(data):
	nrow = data.shape[0]
	m_mean, m_peak, m_r_mean, m_min_r, m_peak_r = [], [], [], [], []
	for i in range(nrow):
		m_mean.append(d_character(data[i,:])[0])
		m_peak.append(d_character(data[i,:])[1])
		m_r_mean.append(d_character(data[i,:])[2])
		m_min_r.append(d_character(data[i,:])[3])
		m_peak_r.append(d_character(data[i,:])[4])
	r1 = np.mean(np.array(m_mean))
	r2 = np.max(np.array(m_peak))
	r3 = np.mean(np.array(m_r_mean))
	r4 = np.min(np.array(m_min_r))
	r5 = np.max(np.array(m_peak_r))
	return r1, r2, r3, r4, r5

def m_character(file,start,end):
	data = pro_data(file,start,end)[0]
	nrow = data.shape[0]
	m_mean, m_peak, m_r_mean, m_min_r, m_peak_r = [], [], [], [], []
	for i in range(nrow):
		m_mean.append(d_character(data[i,:])[0])
		m_peak.append(d_character(data[i,:])[1])
		m_r_mean.append(d_character(data[i,:])[2])
		m_min_r.append(d_character(data[i,:])[3])
		m_peak_r.append(d_character(data[i,:])[4])
	r1 = np.mean(np.array(m_mean))
	r2 = np.max(np.array(m_peak))
	r3 = np.mean(np.array(m_r_mean))
	r4 = np.min(np.array(m_min_r))
	r5 = np.max(np.array(m_peak_r))
	return r1, r2, r3, r4, r5

def multi_m_character(file,start,end):
	data = pro_data(file,start,end)[0]
	time = pro_data(file,start,end)[1]
	days = time.shape[0]
	months = []
	for i in range(days):
		dd = datetime.datetime.strptime(time[i,0], "%Y/%m/%d")
		months.append((dd.year, dd.month))
	new_months = list(set(months))
	new_months.sort(key=months.index)
	num_month = len(new_months)
	index_list = [[] for i in range(num_month)]
	for m in range(num_month):
		for d in range(days):
			dd = datetime.datetime.strptime(time[d,0], "%Y/%m/%d")
			if dd.year == new_months[m][0] and dd.month == new_months[m][1]:
				index_list[m].append(d)
	data_list = []
	result = []
	for i in range(num_month):
		data_list.append(data[index_list[i],:])
		mon_data = data[index_list[i],:]
		result.append(list(m_pre_character(mon_data)))
	# new_months, data_list
	return new_months, result

if __name__ == '__main__':
	m_mean, m_peak, m_r_mean, m_min_r, m_peak_r = m_character(
		"yunnan_day_电力电量类", "2013/1/1","2013/1/31")
	print(m_mean, m_peak, m_r_mean, m_min_r, m_peak_r)
	months, result = multi_m_character("yunnan_day_电力电量类", "2013/1/1","2013/3/31")
	print(result)
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

def y_pre_load_cons(data):
	# # data shape: np array (8760,)
	data = data.reshape((1,-1)).flatten()
	data = -np.sort(-data)
	x = range(1,len(data)+1,1)

	fig = plt.figure()
	plt.plot(x,data)
	plt.show()
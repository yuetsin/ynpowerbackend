%% Step1: 导入相应数据 ,'b2:Y11'
clc
clear
load = xlsread('云南丰水期2020.xlsx','中位');
power = 1476433;
maxload = 72442;
forecast_result=Fractal_main(load,power,maxload);
clc;
clear;
% global Tyear startyear endyear
% %%基本信息输入
% %%info为8760*N的矩阵，N为历史年份数目；cityname=城市名，premaxload为预测的最大负荷（MW）
% cityname=input('请输入城市名称：','s');
info=xlsread('E:\项目\云南\华东预测程序数据（Matlab）\指数平滑法数据\yunnan_8760.xlsx').';
info = info(2:8761,2:8);
% startyear=input('请输入数据库起始年份：');
% xyear=find(2013==info(1,:));
% endyear=input('请输入数据库截止年份：');
% yyear=find(2019==info(1,:));
%numyear=endyear-startyear+1;
Tyear=2020;
%T=Tyear-endyear;
premaxload=70000;
%%程序调用
P1=seek41(info,'云南',premaxload,Tyear,2013,2019);%%结果输出,输出结果为8760*1的列向量
% xlswrite('C:\Users\oodil\Desktop\项目\云南\华东预测程序数据（Matlab）\指数平滑法数据\数据预测.xlsx',P1,cityname,'A1:A8760');
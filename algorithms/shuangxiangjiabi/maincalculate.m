clc;
clear;
%%基本信息输入
global numyear
% global season cityname startyear endyear Tyear info numyear
% season=input('请输入sheet名称：','s');
% cityname=input('请输入城市名称：','s');
% startyear=input('请输入数据库起始年份：');
% endyear=input('请输入数据库截止年份：');
% numyear=endyear-startyear+1;
% Tyear=input('请输入待预测的年份：');
actress1='E:\项目\云南\华东预测程序数据（Matlab）\双向夹逼法数据\yunnan_year_loadchara_jiabi';
% path1=strcat(actress1,cityname);
%%数据库的生成
info=xlsread(actress1);
info = info.';
numyear=7;
%%最大负荷、最小负荷、预测日电量预测%%
premaxload=65000;
pretotal=1300000;
%%调用函数计算
load=seek32(info,premaxload,pretotal);
%%输出数据
% xlswrite('C:\Users\oodil\Desktop\项目\云南\华东预测程序数据（Matlab）\双向夹逼法数据\数据预测_华东.xlsx',load,season,'A1:A24');
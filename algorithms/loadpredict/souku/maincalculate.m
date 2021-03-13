clc;
clear;
%%基本信息输入
% global season cityname startyear endyear Tyear
% season=input('请输入sheet名称：','s');
% cityname=input('请输入城市名称：','s');
% startyear=input('请输入数据库起始年份：');
% endyear=input('请输入数据库截止年份：');
% Tyear=input('请输入待预测的年份：');
%%最大负荷、最小负荷、预测日电量预测%%
premaxload=65000;
pretotal=1300000;
pregamma=0.9;
prebeta=0.7;
%%数据库读取
actress1='E:\项目\云南\华东预测程序数据（Matlab）\搜库法数据\yunnan_year_loadchara_souku';
% path1=strcat(actress1,cityname);
%%将典型日信息存入info中

% info=xlsread(path1,season);
info = xlsread(actress1);
% [item year]=size(info);
startyearNum=find(2013==info(:,1));
endyearNum=find(2018==info(:,1));
numyear=endyearNum-startyearNum+1;
Maxload=info(startyearNum:endyearNum,26).';
Total=info(startyearNum:endyearNum,27).';
gamma=info(startyearNum:endyearNum,28).';
beta=info(startyearNum:endyearNum,29).';
info=info(startyearNum:endyearNum,1:25).';
%%调用函数计算
load=seek22(info,premaxload,gamma,pregamma,prebeta);
%%输出数据
% xlswrite('E:\项目\云南\华东预测程序数据（Matlab）\搜库法数据\数据预测_福建.xlsx',load,season,'A1:A24');
function [forecast_result,H,A,C,D,E,F]=interation(load_peryear_adjusted,x1,interation_num,initial_point)
[year_num,hour_num]=size(load_peryear_adjusted); %获取历史年份以及分段小时数：这里hour_num =8;
n=length(x1); %插值点的长度
x=ones(year_num,1)*x1; %9*8矩阵，每年的插值点横坐标
IFS_num=n-1; %迭代函数系的个数，N-1哥
y=zeros(year_num,n); %9*8矩阵，对应插值点的负荷值
a=zeros(year_num,IFS_num); %仿射变换的参数
c=zeros(year_num,IFS_num);
d=zeros(year_num,IFS_num);
e=zeros(year_num,IFS_num);
f=zeros(year_num,IFS_num);
H=Hurst_calculation(load_peryear_adjusted); %求解分形系数

%% 求解 仿射变换参数
for i=1:year_num
    y(i,:)=load_peryear_adjusted(i,x(i,:));
    [a(i,:),c(i,:),d(i,:),e(i,:),f(i,:)]=fractal_IFS(x(i,:),y(i,:),H(1));
end
%% 通过对各列仿射变换参数做平均，得到总的迭代函数系
A=mean(a,1);
C=mean(c,1);
D=mean(d,1);
E=mean(e,1);
F=mean(f,1);
%% 吸引子
attrator_before=initial_point;
attractor_num=1;
% attrator_after =[];
for k=1:interation_num
    attrator_after=zeros(2,attractor_num*IFS_num);
    for i=1:IFS_num
        attrator_after(:,((i-1)*attractor_num+1):(i*attractor_num))=[A(i),0;C(i),D(i)]*attrator_before+[E(i);F(i)]*ones(1,attractor_num);%一个点将扩展成IFS_num个点          
    end
    attrator_before=attrator_after;
    %Edit by phq
    %attrator_after = [attrator_before,attrator_after];
    attractor_num=size(attrator_before,2); %返回后来吸引子的列数
end
%% 吸引子第一行为x坐标，第二行为y坐标
attractor_num=size(attrator_after,2); %返回后来吸引子的列数
attrator_x=attrator_after(1,:);
attrator_y=attrator_after(2,:);

hour_temp=zeros(1,attractor_num);
load_temp=zeros(1,attractor_num);
forecast_result=zeros(1,hour_num);
hour_max=max(attrator_x);
for i=1:attractor_num
    [hour_temp(i),ID]=min(attrator_x);
    load_temp(i)=attrator_y(ID);
    attrator_x(ID)=hour_max+1;
end
forecast_result(1)=load_temp(1);
% hour_temp
for i=2:hour_num
    ID1=find(hour_temp<=i);
    forecast_result(i)=load_temp(ID1(length(ID1)));
end

    


    
    

function forecast_result=Fractal_main(load,power,max_load)
%------------------输入------------------
%load——历史年负荷曲线(至少3年数据）！！注意：load的单位是MW，为n*24的矩阵，n表示历史年数（行），24表示24个时刻（列）
%power——预测年典型日用电量预测值   ！！注意：power的单位是亿千瓦
%max_load——预测年典型日最大负荷预测值  ！！注意：power的单位是MW
%------------------输入------------------
%forecast_result——预测年典型日负荷曲线 ！！注意：forecast_result的单位是MW

section=3; %分为三段，每个负荷点都是插值点
[year_num,hour_num]=size(load); %获取历史年典型日负荷曲线的维数
forecast1=zeros(1,year_num); %
n=hour_num/section; %8小时一段
x=ones(year_num,1)*(1:n); %9*8矩阵，元素值从1到8
IFS_num=n-1;  %迭代函数系个数，或者说仿射变换的个数，7
y=zeros(year_num,n); %9*8矩阵，插值点对应负荷值？？
a=zeros(year_num,IFS_num); %仿射变换的参数，每一个仿射变换对应一个参数，每年对应一个分形曲线
c=zeros(year_num,IFS_num);
d=zeros(year_num,IFS_num);
e=zeros(year_num,IFS_num);
f=zeros(year_num,IFS_num);
interation_num=4; %Nmax，求解吸引子时的最大迭代次数
k=0;
for j=2:(year_num*n-1)
    if mod(year_num*n,j)==0
        k=k+1;
        GYueShu(k)=j;
        %Edit by PHQ
%         n(k)=j;
    end
end %n(k)为9*8的约数
num_n=length(GYueShu);  %9*8含有多少个约数，即有多少种不同时间尺度的分法
% Hurst=zeros(num_n-1,2);%用于OLS的求解
 Hurst=zeros(num_n,2);%用于OLS的求解
load_Hurst=reshape(load(1:year_num,:)',1,[]);%变成一个长时间序列，一维
RS=zeros(1,num_n); %RS分析法
for i=1:num_n
    num_Ia=hour_num*year_num/GYueShu(i);
    Ia=zeros(num_Ia,GYueShu(i));
    RIa=zeros(num_Ia,1);
    SIa=zeros(num_Ia,1);
    for j=1:num_Ia
        Ia(j,:)=load_Hurst((j-1)*GYueShu(i)+1:j*GYueShu(i));
        ea=mean(Ia(j,:));
        Xka=Ia(j,:)*triu(ones(GYueShu(i),GYueShu(i)),0)-ea*(1:GYueShu(i));
        RIa(j)=max(Xka)-min(Xka);
        SIa(j)=std(Ia(j,:),1);
    end
    ID0=find(SIa==0);
    SIa(ID0)=1;
    RIa(ID0)=0;
    RS(i)=sum(RIa./SIa)/(num_Ia-length(ID0));
    if i>1
        Hurst(i-1,:)=polyfit(log(GYueShu(1:i)),log(RS(1:i)),1);
    end
end
disp(Hurst)
H=max(Hurst(:,1));

for j=1:section %对各段进行分形插值
    %initial_point=load(year_num,(j-1)*n+1)
 %   [forecast1((j-1)*n+1:j*n),~,~,~,~,~,~]=interation(load(:,(j-1)*n+1:j*n),1:n,4,[1,load(year_num,(j-1)*n+1)]);
     [forecast1((j-1)*n+1:j*n),~,~,~,~,~,~]=interation(load(:,(j-1)*n+1:j*n),1:n,interation_num,[1;load(year_num,(j-1)*n+1) ]);
end
forecast2=forecast1.*max_load/max(forecast1); %按最大负荷修正
forecast_result=forecast2.*(1+(power-sum(forecast2))/sum(forecast2)); %按典型日用电量预测值修正
end




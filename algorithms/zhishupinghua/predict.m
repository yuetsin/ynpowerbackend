%%根据二次指数平滑法预测未来年的电量、最大负荷
function z=predict(x,y,endy)
at=0;
bt=0;
year=y-endy;
num=length(x);
s1=zeros(num,1);
s2=zeros(num,1);
a=0.5;
s1(1,1)=x(1);
for i=2:num
    s1(i,1)=a*x(i)+(1-a)*s1(i-1,1);
end
s2(1,1)=s1(1,1);
for i=2:num
    s2(i,1)=a*s1(i,1)+(1-a)*s2(i-1,1);
end
at=2*s1(num,1)-s2(num,1);
bt=a/(1-a)*(s1(num,1)-s2(num,1));
z=(at+bt*year);

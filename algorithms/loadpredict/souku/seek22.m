function load=seek22(info,premaxload,gamma,pregamma,prebeta)
global endyear startyear
%%寻找基准曲线
numyear=endyear-startyear+1;
value=abs(gamma-pregamma*ones(1,numyear));
disp(value);
disp(find(value==min(value))+1);
yearfind=info(1,find(value==min(value)))
if(yearfind~=0)
    num=size(info,2);
    for j=1:num
        if(info(1,j)==yearfind)
            loadcurve=info(2:25,j);
        end
    end
end
%%对基准曲线进行修正
base=max(loadcurve)*ones(24,1);
loadcurve2=loadcurve./base;
loadcurve3=dsort(loadcurve2);
for kk=1:length(loadcurve3)
    order(kk,1)=find(loadcurve3(kk)==loadcurve2);
end
for ii=1:23
    X00(ii)=loadcurve3(ii)-loadcurve3(ii+1);
end    
X0=X00';
W=zeros(23,1);
A=[23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1;1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1];
b=[24*(1-pregamma);1-prebeta];
ee=2e-5;
ffflag=1;
k2=1;    
while(ffflag>ee)
    V=inv(A*A')*(b-A*(X0+W));
    Z=X0+A'*V;
    for i=1:23;
        if Z(i)<0 
            W(i)=-Z(i);
            Z(i)=0;
        else W(i)=0;
        end
    end
        k2=k2+1;
  ffflag=norm(A*Z-b,2)/norm(b,2);
end
   c=Z-X0-W-A'*V;
    dd=A*Z-b;   
    ex=diag(W)*Z;
%%预测曲线恢复
y1=zeros(24,1);
d=zeros(24,1);
y1(1)=1;
for n=1:23
    y1(n+1)=y1(n)-Z(n);
end
for m=1:24
    d(order(m))=y1(m);
end
%%实际值曲线计算
load=premaxload*d;



function Hurst_max=Hurst_calculation(load_peryear)
[year_num,num_hour]=size(load_peryear);
k=0;
for j=2:(year_num*num_hour-1)
    if mod(year_num*num_hour,j)==0
        k=k+1;
        n(k)=j;
    end
end
num_n=length(n);
Hurst=zeros(num_n-1,2);
load=reshape(load_peryear(1:year_num,:)',1,[]);
RS=zeros(1,num_n);
for i=1:num_n
    num_Ia=num_hour*year_num/n(i);
    Ia=zeros(num_Ia,n(i));
    RIa=zeros(num_Ia,1);
    SIa=zeros(num_Ia,1);
    for j=1:num_Ia
        Ia(j,:)=load((j-1)*n(i)+1:j*n(i));
        ea=mean(Ia(j,:));
        Xka=Ia(j,:)*triu(ones(n(i),n(i)),0)-ea*(1:n(i));
        RIa(j)=max(Xka)-min(Xka);
        SIa(j)=std(Ia(j,:),1);
    end
    ID0=find(SIa==0);
    SIa(ID0)=1;
    RIa(ID0)=0;
    RS(i)=sum(RIa./SIa)/(num_Ia-length(ID0));
    if i>1
        Hurst(i-1,:)=polyfit(log(n(1:i)),log(RS(1:i)),1);
    end
end
Hurst_max=zeros(1,2);
[Hurst_max(1),ID]=max(Hurst(:,1));
Hurst_max(2)=Hurst(ID,2);


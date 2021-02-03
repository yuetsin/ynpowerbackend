function[a,c,d,e,f]=fractal_IFS(x,y,H)
n=length(x);
a=zeros(1,n-1);
c=zeros(1,n-1);
e=zeros(1,n-1);
f=zeros(1,n-1);
xl=x(n)-x(1);
for i=1:n-1
a(i)=(x(i+1)-x(i))/xl;
end
d=ones(1,n-1)*(1/(sum(a.^(1-H))));
for i=1:n-1
    e(i)=(x(n)*x(i)-x(1)*x(i+1))/xl;
    c(i)=(y(i+1)-y(i)-d(i)*(y(n)-y(1)))/xl;
    f(i)=((x(n)*y(i)-x(1)*y(i+1))-d(i)*(x(n)*y(1)-x(1)*y(n)))/xl;
end
    
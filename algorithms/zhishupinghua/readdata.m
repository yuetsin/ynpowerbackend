clc
clear
array = zeros(7,8760);

for i = 1:8760
    data = loadjson(getData("yunnan_year_dianlidianliang-8760",num2str(i-1),"2013","2019"));
    array(1,i) = data.("x0x32_013");
    array(2,i) = data.("x0x32_014");
    array(3,i) = data.("x0x32_015");
    array(4,i) = data.("x0x32_016");
    array(5,i) = data.("x0x32_017");
    array(6,i) = data.("x0x32_018");
    array(7,i) = data.("x0x32_019");
end
info = array.';
Tyear=2020;
%T=Tyear-endyear;
premaxload=70000;
%%程序调用
P1=seek41(info,'云南',premaxload,Tyear,2013,2019);

clc
clear
global endyear startyear
start = 2013;
ending = 2018;
premaxload=65000;
pretotal=1300000;
pregamma=0.9;
prebeta=0.7;
startyear = start;
endyear = ending;
year = ending-start;
array = zeros(year,25);
ga = zeros(year,1);
columns = ["m_01", "m_02", "m_03","m_04","m_05","m_06","m_07","m_08","m_09","m_10","m_11","m_12","m_13","m_14","m_15","m_16","m_17","m_18","m_19","m_20","m_21","m_22","m_23","m_24"
];
col = 'm_01,m_02,m_03,m_04,m_05,m_06,m_07,m_08,m_09,m_10,m_11,m_12,m_13,m_14,m_15,m_16,m_17,m_18,m_19,m_20,m_21,m_22,m_23,m_24,gamma';

% array(1:6,1)=["2013","2014","2015","2016","2017","2018"];
for i = 1:year
    array(i,1) = start+i-1;
end
for i = 1:24
    data = loadjson(getData("yunnan_year_loadchara_souku",columns(i),num2str(start),num2str(ending)));
    array(1,i+1) = data.("x0x32_013");
    array(2,i+1) = data.("x0x32_014");
    array(3,i+1) = data.("x0x32_015");
    array(4,i+1) = data.("x0x32_016");
    array(5,i+1) = data.("x0x32_017");
    array(6,i+1) = data.("x0x32_018");
end
s = getData("yunnan_year_loadchara_jiabi",col,num2str(start),num2str(ending));
num = length(s);
for i = 1:num
    a = s(i);
    x = str2num(a{1,1}{1,1})-start+1;
    if length(a{1,1}{2,1}) == 4
        y = str2num(a{1,1}{2,1}(3:4))+1;
        array(x,y) = a{1,1}{3,1};
    else
        ga(x,1) = a{1,1}{3,1};
    end   
    
end


% gamma = loadjson(getData("yunnan_year_loadchara_souku","gamma","2013","2018"));
% ga(1,1) = gamma.("x0x32_013");
% ga(2,1) = gamma.("x0x32_014");
% ga(3,1) = gamma.("x0x32_015");
% ga(4,1) = gamma.("x0x32_016");
% ga(5,1) = gamma.("x0x32_017");
% ga(6,1) = gamma.("x0x32_018");

info = array.';
gamma = ga.';
load=seek22(info,premaxload,gamma,pregamma,prebeta);

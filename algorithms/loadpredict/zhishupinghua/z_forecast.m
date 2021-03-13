function result = z_forecast(start, ending, Tyear, premaxload,file)
    number = 500;
    data = [];
    
    for point = 0:number:8000
        columns = [];
        for k = point:point+number-1
            columns = [columns num2str(k)];
            if k < point+number-1
                columns = [columns ','];
            end
        end
        arr = process(columns,start,ending,number,point,file);
        data = [data,arr];
    end
    
    columns = [];
    for k = 8500:8759
        columns = [columns num2str(k)];
        if k < 8759
            columns = [columns ','];
        end
    end
    arr = process(columns,2013,2019,260,8500,file);
    data = [data,arr];
    
    info = data.';
    
    result = seek41(info,'ÔÆÄÏ',premaxload,Tyear,start,ending);
end


function [array] = process(col,start,endding,number,point,file)
array = zeros(endding-start+1,number);
s = getData(file,col,num2str(start),num2str(endding));
num = length(s);
for i = 1:num
    a = s(i);
    x = str2num(a{1,1}{1,1})-start+1;
    y = str2num(a{1,1}{2,1})+1-point;
    array(x,y) = a{1,1}{5,1};
end
end



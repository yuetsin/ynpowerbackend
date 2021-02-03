function status = getData(location, dataName, startTime, endTime)
    import matlab.net.*
    import matlab.net.http.*
    
    r = RequestMessage;
    uri = URI(sprintf('https://ynpowerbackend.dclab.club/getDataJson?dataName=%s&startTime=%s&endTime=%s&location=%s', dataName, startTime, endTime, location)); 
    resp = send(r,uri);
    status = resp.Body.Data.data;
end




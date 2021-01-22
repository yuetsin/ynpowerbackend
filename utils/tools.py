from datetime import datetime

def formateTimeString(t, grain):
    if grain == 'day':
        timet = datetime.strptime(t, '%Y/%m/%d')
        timestr = timet.strftime('%Y/%m/%d')
    elif grain == 'mouth':
        timet = datetime.strptime(t, '%Y/%m')
        timestr = timet.strftime('%Y/%m')
    elif grain == 'hour':
        timet = datetime.strptime(t, '%Y/%m/%d %H')
        timestr = timet.strftime('%Y/%m/%d %H')
    elif grain == 'min':
        timet = datetime.strptime(t, '%Y/%m/%d %H:%M')
        timestr = timet.strftime('%Y/%m/%d %H:%M')
    elif grain == 'sec':
        timet = datetime.strptime(t, '%Y/%m/%d %H:%M:%S')
        timestr = timet.strftime('%Y/%m/%d %H:%M:%S')
    else:
        timet = datetime.strptime(t, '%Y')
        timestr = timet.strftime('%Y')
    # print(timestr)
    return timestr

from .algorithm import y_character, typical_day, y_load, y_load_cons, multi_y_character
from .day import d_character, day_plot, multi_d_character
from .month import m_character, multi_m_character


#年负荷特性
def yearfeature(start, end, datasource="yunnan_day_电力电量类"):
    result = multi_y_character(datasource, start, end)
    print(result)
    re = []
    for i in range(len(result[0])):
        temp = {
            'year': result[0][i],
            'yearMaxPayload': int(result[1][i][0]),
            'yearMinPayload': int(result[1][i][1]),
            'yearAverageDailyPayloadRate': round(result[1][i][2],3),  # ,
            'yearMaxPeekValleyDiff': round(result[1][i][3],3),  # ,
            'yearRate': round(result[1][i][4],3),  # ,
            'seasonImbaRate': round(result[1][i][5],3),  # ,
            'monthImbaRate': round(result[1][i][6],3),  #
        }
        re.append(temp)
    return re
    # max_l,min_l,mean_l,max_p2v,y_ratio, s_unbalance, m_unbalance = y_character(datasource, start, end)
    # result = {
    #     'yearMaxPayload': max_l,
    #     'yearMinPayload': min_l,
    #     'yearAverageDailyPayloadRate': mean_l,
    #     'seasonImbaRate': s_unbalance,
    #     'monthImbaRate': m_unbalance,
    #     'yearMaxPeekValleyDiff': max_p2v,
    #     'yearRate': y_ratio
    # }
    # return result
#典型日
def typicalDay(start, end, season, datasource="yunnan_day_电力电量类"):
    return typical_day(datasource, start, end, season)
#年负荷曲线
def yearLoad(start, end, datasource="yunnan_day_电力电量类"):
    result = y_load(datasource, start, end)
    return result
#年持续负荷曲线
def yearLoadCon(start, end, datasource="yunnan_day_电力电量类"):
    result = y_load_cons(datasource, start, end)
    return result
#日负荷特征
def dayFeature(start, end, datasource="yunnan_day_电力电量类"):
    result = multi_d_character(datasource, start, end)
    # print(result[0].tolist())
    re = [] #d_max, d_mean, d_min, d_r, d_m_r, peak, peak_r
    for i in range(len(result[0].tolist())):
        temp = {
            'day': result[0][i][0],
            'dayMaxPayload': int(result[1][i][0]),
            'dayMinPayload': int(result[1][i][2]), #d_min,
            'dayAveragePayload': int(result[1][i][1]), #d_mean,
            'dayPayloadRate': round(result[1][i][3], 3), #d_r,
            'dayMinPayloadRate': round(result[1][i][4],3), #d_m_r,
            'dayPeekValleyDiff': int(result[1][i][5]), #peak,
            'dayPeekValleyDiffRate': round(result[1][i][6],3), #peak_r
        }
        re.append(temp)
    return re
#日负荷曲线
def dayLoad(start, end, datasource="yunnan_day_电力电量类"):
    result = day_plot(datasource, start, end)
    return result.tolist()

#月负荷特性
def monthFeature(start, end, datasource="yunnan_day_电力电量类"):
    result = multi_m_character(datasource, start, end)
    re = []
    for i in range(len(result[0])):
        temp = {
            'month': str(result[0][i][0]) + "/" +str(result[0][i][1]),
            'monthAverageDailyPayload': int(result[1][i][0]),
            'monthMaxPeekValleyDiff': int(result[1][i][1]),
            'monthAverageDailyPayloadRate': round(result[1][i][2],3),
            'monthMinPayloadRate': round(result[1][i][3],3),
            'monthMaxPeekValleyDiffRate': round(result[1][i][4],3),
        }
        re.append(temp)
    return re
    # m_mean, m_peak, m_r_mean, m_min_r, m_peak_r = m_character(datasource, start, end)
    # result = {
    #     'monthAverageDailyPayload': m_mean,
    #     'monthMaxPeekValleyDiff': m_peak,
    #     'monthAverageDailyPayloadRate': m_r_mean,
    #     'monthMinPayloadRate': m_min_r,
    #     'monthMaxPeekValleyDiffRate': m_peak_r
    # }
    # return result


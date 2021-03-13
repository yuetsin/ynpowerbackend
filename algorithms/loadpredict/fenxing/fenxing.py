from algorithms.loadpredict.fenxing.fx.for_redistribution_files_only import fx
import numpy as np

def fenxingpre(start, ending, power,maxload,file="yunnan_year_loadchara_test"):
    start = float(start)
    ending = float(ending)
    power = float(power)
    maxload = float(maxload)
    f = fx.initialize()
    re = f.fracal_forcast(start, ending, power,maxload,file)
    re = np.asarray(re)
    re = re.flatten()

    return re.tolist()

if __name__ == '__main__':
    start = 2013;
    ending = 2019;

    power = 1476433;
    maxload = 72442;

    file = "yunnan_year_loadchara_test";

    re = fenxingpre(start, ending, power,maxload,file)
    print(re)
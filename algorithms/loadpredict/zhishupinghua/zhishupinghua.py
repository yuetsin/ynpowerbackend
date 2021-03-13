from algorithms.loadpredict.zhishupinghua.zsph.for_redistribution_files_only import zsph
import numpy as np

def zhishupinghua(start, ending, Tyear, premaxload, file="yunnan_year_dianlidianliang-8760"):
    start = float(start)
    ending = float(ending)
    Tyear = float(Tyear)
    premaxload = float(premaxload)
    zs = zsph.initialize()
    re = zs.z_forecast(start, ending, Tyear, premaxload, file)
    re = np.asarray(re)
    re = re.flatten()
    return re.tolist()



if __name__ == '__main__':
    start = 2013
    ending = 2019
    Tyear = 2020
    premaxload = 70000
    file = "yunnan_year_dianlidianliang-8760"
    re = zhishupinghua(start, ending, Tyear, premaxload, file);

    print(re)
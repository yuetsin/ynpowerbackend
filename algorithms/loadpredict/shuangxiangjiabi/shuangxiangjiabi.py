from algorithms.loadpredict.shuangxiangjiabi.sxjb.for_redistribution_files_only import sxjb
import numpy as np

def shuangxiangjiabi(start, ending, premaxload, pretotal, file="yunnan_year_loadchara_jiabi"):
    start = float(start)
    ending = float(ending)
    pretotal = float(pretotal)
    premaxload = float(premaxload)
    sx = sxjb.initialize()
    re = sx.j_forecast(start, ending, premaxload, pretotal, file)
    re = np.asarray(re)
    re = re.flatten()
    return re.tolist()


if __name__ == '__main__':
    start = 2013
    ending = 2018
    premaxload = 65000
    pretotal = 1300000
    file = "yunnan_year_loadchara_jiabi"

    f = shuangxiangjiabi(start, ending, premaxload, pretotal, file);
    print(f)


from algorithms.loadpredict.souku.sk.for_redistribution_files_only import sk
import numpy as np

def soukupre(start, ending, premaxload, pretotal,pregamma,prebeta,file="yunnan_year_loadchara_souku"):
    start = float(start)
    ending = float(ending)
    pretotal = float(pretotal)
    premaxload = float(premaxload)
    prebeta = float(prebeta)
    pregamma = float(pregamma)
    skx = sk.initialize()
    re = skx.main(start, ending, premaxload, pretotal,pregamma,prebeta,file)
    re = np.asarray(re)
    re = re.flatten()

    return re.tolist()


if __name__ == '__main__':
    start = float(2013)
    ending = float(2018)
    premaxload = float(65000)
    pretotal = float(1300000)
    pregamma = float(0.9)
    prebeta = float(0.7)
    file = "yunnan_year_loadchara_souku"
    re = soukupre(start, ending, premaxload, pretotal,pregamma,prebeta,file)
    print(re)
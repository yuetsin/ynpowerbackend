from dao.interface import *

def insertAlgorithmReusltController(content, tag):
    re = insertAlgorithmResult(content, tag)
    return re

def getAlgorithmReusltController(tags):
    re = getAlgorithmResultByTag(tags)
    return re
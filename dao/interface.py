import sqlalchemy as db
import json
class Database():
    # replace the user, password, hostname and database according to your configuration according to your information
    engine = db.create_engine('postgresql://dclab:dclab@202.120.40.111/electric')
    def __init__(self):
        self.connection = self.engine.connect()
        print("DB Instance created")

# 示例：   print(getDataJson("曲靖GDP数据","2010-10-20","2010-10-21"))
# 时间请保证均为两位，例如2019年2月1日，即2019-02-01
def getDataJson(dataName,startTime,endTime):
    d = Database()
    resultDict = d.connection.execute("select * from data where dataname='%s'"%(dataName)).first()[1]
    assert isinstance(resultDict,dict)
    matchKeys = []
    for key in resultDict.keys():
        if startTime <= key < endTime:
            matchKeys.append(key)
    matchKeys.sort()
    newDict = {}
    for key in matchKeys:
        newDict[key] = resultDict[key]
    resultJsonStr = json.dumps(newDict)
    return resultJsonStr


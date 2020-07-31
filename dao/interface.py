import sqlalchemy as db
import json
import pandas as pd



class Database():
    # replace the user, password, hostname and database according to your configuration according to your information
    engine = db.create_engine('postgresql://postgresadmin:admin123@192.168.1.108:32345/electric')

    def __init__(self):
        self.connection = self.engine.connect()
        print("DB Instance created")


# 示例：   print(getDataJson("曲靖GDP数据","2010-10-20","2010-10-21"))
# 时间请保证均为两位，例如2019年2月1日，即2019-02-01
def getDataJson(dataName, startTime, endTime):
    d = Database()
    resultDict = d.connection.execute("select * from data where dataname='%s'" % (dataName)).first()[1]
    assert isinstance(resultDict, dict)
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


def insertData(data):
    engine = db.create_engine('postgresql://postgresadmin:admin123@192.168.1.108:32345/electric')
    pd.io.sql.to_sql(data, 'electric_data', engine, index=False, if_exists='append')
    return


def getData(dataName, startTime, endTime, grain, area):
    d = Database()
    resultDict = d.connection.execute(
        "select * from electric_data where dataname='%s' and grain = '%s' and area = '%s' and datatime >= '%s' and datatime <= '%s' " % (
        dataName, grain, area, startTime, endTime)).fetchall()

    newDict = {}
    for r in resultDict:
        newDict[r[0]] = r[2]
    resultJsonStr = json.dumps(newDict)
    return resultJsonStr

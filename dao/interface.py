import sqlalchemy
import sqlalchemy as db
import json
import pandas as pd
import numpy as np
import psycopg2
from utils.tools import formateTimeString


class Database():
    # replace the user, password, hostname and database according to your configuration according to your information
    engine = db.create_engine('postgresql://postgresadmin:admin123@192.168.1.108:32345/electric')
    #engine = db.create_engine('postgresql://postgres:ynpower@localhost:5432/electric')

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
    #engine = db.create_engine('postgresql://postgres:ynpower@localhost:5432/electric')
    #pd.io.sql.to_sql(data, 'electric_data', engine, index=False, if_exists='replace', dtype={'datatime': sqlalchemy.Date()})
    pd.io.sql.to_sql(data, 'electric_data', engine, index=False, if_exists='replace')
    return

def addPowerData(data, area, grain, kind):
    #conn = psycopg2.connect(dbname="electric", user="postgres", password="ynpower", host="127.0.0.1", port="5432")
    conn = psycopg2.connect(dbname="electric", user="postgresadmin", password="admin123", host="dclab.club", port="32345")
    cur = conn.cursor()
    values = []
    insertjoin = " "
    x, y = data.shape
    # print(data.columns)
    header = [i for i in data.columns]
    for i in range(x):
        datatime = data.iloc[i][0]
        datatime = formateTimeString(datatime, grain)
        for j in range(1, y):
            if np.isnan(data.iloc[i][j]):
                continue
            # print(data.iloc[i][j], header[j])
            values.append("INSERT INTO electric_data VALUES('{}', '{}', {}, '{}', '{}', '{}') on conflict on constraint unique_all_cons do update set datavalue={};".format(
                    datatime, header[j],data.iloc[i][j], grain, area, kind, data.iloc[i][j]))
    # for index, row in data.iterrows():
    #     print(row, area, grain, kind)
    insert = insertjoin.join(values)
    # print(insert)
    cur.execute(insert)
    conn.commit()
    conn.close()

def getData(location, dataName, startTime, endTime):
    l = location.split("_")
    grain = l[1]
    area = l[0]
    kind = l[2]
    d = Database()
    startTime = formateTimeString(startTime, grain)
    endTime = formateTimeString(endTime, grain)
    sql = "select * from electric_data where dataname='%s' and grain = '%s' and area = '%s' and datatime >= '%s' and datatime <= '%s'  and kind = '%s'" % (
        dataName, grain, area, startTime, endTime, kind)
    print(sql)
    resultDict = d.connection.execute(sql).fetchall()
    newDict = {}
    for r in resultDict:
        # print(r)
        newDict[r[0]] = r[2]
    resultJsonStr = json.dumps(newDict)
    return resultJsonStr


def getUserByPsAndName(username, password):
    conn = psycopg2.connect(dbname="electric", user="postgresadmin", password="admin123", host="192.168.1.108", port="32345")
    cur = conn.cursor()
    cur.execute("select count(*) from electric where username = '{}' and password = '{}'".format(username, password))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    if rows > 0:
        return True
    else:
        return False



def insertAlgorithmResult(result, tag):
    conn = psycopg2.connect(dbname="electric", user="postgresadmin", password="admin123", host="dclab.club",
                            port="32345")
    cur = conn.cursor()
    result = json.dumps(result)
    sql = "INSERT INTO program (tag, content) VALUES('{}', '{}') on conflict on constraint unique_tag do update set content='{}';".format(tag, result, result)
    # print(sql)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return

def getAlgorithmResultByTag(tags):
    conn = psycopg2.connect(dbname="electric", user="postgresadmin", password="admin123", host="dclab.club",
                            port="32345")
    cur = conn.cursor()
    tagslist = tags.split(',')
    tag = ""
    for i in range(len(tagslist)):
        tag += "'" + tagslist[i] + "'"
        if i != len(tagslist) - 1:
            tag += ","
    sql = "select tag, content from program where tag in ({})".format(tag)
    # print(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows





if __name__ == '__main__':
    conn = psycopg2.connect(dbname="electric", user="postgresadmin", password="admin123", host="192.168.1.108",
                            port="32345")
    cur = conn.cursor()
    grain = "year"
    area = "yunnan"
    kind = "test"
    data = [('2018', 'GDPperpop', 37136.0, 'year', 'yunnan', 'test'), ('2018', 'GDP', 17881.12, 'year', 'yunnan', 'test'), ('2018', 'population', 4829.5, 'year', 'yunnan', 'test'), ('2020', 'populations', 4829.5, 'year', 'yunnan', 'test')]
    sql = "SELECT * FROM electric_data where grain = '{}' and area = '{}' and kind = '{}'".format(
        grain, area, kind)
    cur.execute(sql)
    rows = cur.fetchall()

    print(rows)
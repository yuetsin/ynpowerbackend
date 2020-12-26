import sqlalchemy
import sqlalchemy as db
import json
import pandas as pd
import psycopg2


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

def addPowerData(data):
    #conn = psycopg2.connect(dbname="electric", user="postgres", password="ynpower", host="127.0.0.1", port="5432")
    conn = psycopg2.connect(dbname="electric", user="postgresadmin", password="admin123", host="192.168.1.108", port="32345")
    cur = conn.cursor()
    for index, row in data.iterrows():
        sql = "SELECT * FROM electric_data where datatime = '{}' and dataname = '{}' and grain = '{}' and area = '{}' and kind = '{}'".format(row['datatime'], row['dataname'], row['grain'], row['area'], row['kind'])
        #print(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        if len(rows) > 0:

            cur.execute("UPDATE electric_data SET datavalue={} WHERE datatime = '{}' and dataname = '{}' and grain = '{}' and area = '{}' and kind = '{}'".format(row['datavalue'],  row['datatime'], row['dataname'], row['grain'], row['area'], row['kind']))
            conn.commit()
        else:
            cur.execute("INSERT INTO electric_data VALUES('{}', '{}', {}, '{}', '{}','{}')".format(row['datatime'], row['dataname'], row['datavalue'], row['grain'], row['area'], row['kind']))
            conn.commit()
    conn.close()

def getData(location, dataName, startTime, endTime):
    l = location.split("_")
    grain = l[1]
    area = l[0]
    kind = l[2]
    d = Database()
    sql = "select * from electric_data where dataname='%s' and grain = '%s' and area = '%s' and datatime >= '%s' and datatime <= '%s'  and kind = '%s'" % (
        dataName, grain, area, startTime, endTime, kind)
    print(sql)
    resultDict = d.connection.execute(sql).fetchall()
    newDict = {}
    for r in resultDict:
        print(r)
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
import psycopg2




def getProgramName():
    conn = psycopg2.connect(dbname="electric", user="postgresadmin", password="admin123", host="192.168.1.108",
                            port="32345")
    cur = conn.cursor()
    sql = "select name_id from programname order by name_id desc limit 1"
    cur.execute(sql)
    re = cur.fetchall()
    if len(re) == 0:
        return ""
    else:
        return re['name_id']

def getLastInfo():
    conn = psycopg2.connect(dbname="electric", user="postgresadmin", password="admin123", host="192.168.1.108",
                            port="32345")
    cur = conn.cursor()
    sql = "select * from program order by program_id desc limit 1"
    cur.execute(sql)
    re = cur.fetchall()
    if len(re) == 0:
        return re
    else:
        return re
    conn.commit()
    conn.close()

# def insertInfo(content, name, function):
#     conn = psycopg2.connect(dbname="electric", user="postgresadmin", password="admin123", host="192.168.1.108",
#                             port="32345")
#     cur = conn.cursor()
#     sql = "select program_id from program order by program_id desc limit 1"
#     cur.execute(sql)
#     re = cur.fetchall()
#     if len(re) == 0:
#
#     else:
#         sql = "insert into program(`content`, `name`, `function`) values({}, {}, {}})".format(content, name, function)
#         cur.execute(sql)
#         conn.commit()
#         conn.close()

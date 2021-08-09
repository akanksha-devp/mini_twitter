import pymysql

HOST = "sql6.freemysqlhosting.net"
USER = "sql6429828"
PASS = "ZTFrst7k8C"
DATABASE = "sql6429828"


def db_connection():
    db = pymysql.connect(host=HOST, user=USER, passwd=PASS, db=DATABASE)
    return db

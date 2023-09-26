import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'alwaleedVIP_2003',
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE CRMdb")
print('DB created!')
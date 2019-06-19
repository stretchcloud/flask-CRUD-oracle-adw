import cx_Oracle
import csv

DB = "orcl_high"
DB_USER = "admin"
DB_PASSWORD = "Citi21direct"
con = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB)
cur = con.cursor()

with open("titanic.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for lines in csv_reader:
        cur.execute(
            "insert into titanic (Survived, Pclass, Name, Sex, Age, siblingsOrSpousesAboard, parentsOrChildrenAboard, Fare, uuid) values (:1, :2, :3, :4, :5, :6, :7, :8, :9)",
            (lines))

cur.close()
con.commit()
con.close()
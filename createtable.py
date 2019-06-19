import cx_Oracle


# automonous data warehouse connection constants
# update below with your db credentials
# add wallet files to wallet folder

DB = "orcl_high"
DB_USER = "admin"
DB_PASSWORD = "Citi21direct"


try:
    connection = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB)
    cursor = connection.cursor()
    cursor.execute("create table titanic(Survived varchar2(40 CHAR), Pclass varchar2(40 CHAR), Name varchar2(150 CHAR), \
        Sex varchar2(30 CHAR), Age varchar2(50 CHAR), siblingsOrSpousesAboard varchar2(40 CHAR), parentsOrChildrenAboard varchar2(40 CHAR), Fare varchar2(40 CHAR), uuid varchar2(150 CHAR))")
    print("Table Created successfully")
    
except cx_Oracle.DatabaseError as e: 
    print("There is a problem with Oracle", e) 

finally: 
    if cursor: 
        cursor.close() 
    if connection: 
        connection.close()


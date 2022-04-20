from multiprocessing import Condition
import sqlite3
from datetime import datetime, timedelta


class Records:
    def __init__(self):
        self.conn = sqlite3.connect('my_records.db')
    ########################## Create Table ######################################
    def create(self):
        records_table = """CREATE TABLE IF NOT EXISTS RECORDS(
            Symbol NVARCHAR,
            FullName  NVARCHAR(150),
            LastPrice FLOAT,
            ClosedPrice FLOAT,
            RecordAt DATETIME,
            Type INT,
            isLast BIT
        );"""
        over_all_table = """CREATE TABLE IF NOT EXISTS OVERALL(
            Count  BIGINT,
            Percent  FLOAT,
            RecordAt DATETIME,
        );"""
        user_condition = """CREATE TABLE IF NOT EXISTS USERS(
            ID VARCHAR(50),
            LastCommand NVARCHAR(50),
            RecordAt DATETIME
        );"""
        self.conn.execute(records_table)
        self.conn.execute(over_all_table)
        self.conn.execute(user_condition)

    ########################## Create Table ######################################


    ########################## GET LAST RECORDS #######################
    def get_records(self)-> list:
        q = f"""SELECT * FROM RECORDS WHERE isLast==TRUE;"""
        cursor = self.conn.execute(q)
        records = [row for row in cursor]
        return records
        
    ########################## GET LAST RECORDS #######################



    ################################## CHANGE isLAST STATUS ########################################

    def disable(self, symbol -> str)->None:
        q = f"""UPDATE RECORDS SET isLast = 0 WHERE Symbol = "{symbol}" """
        self.conn.execute(q)
        self.conn.commit()

    ################################## CHANGE iSLAST STATUS ########################################

    ################################## Get Symbol By Name ########################################
    def get_symbol(self, name->str)->str:
        q = f"""SELECT Symbol FROM RECORDS WHERE FullName =="{name}";"""
        cursor = self.conn.execute(q)
        records = [row for row in cursor]
        return records[0]
    ################################## Get Symbol By Name ########################################

    ################################## Get OVERALL ########################################
    def get_overall(self)-> dict:
        q = f"""SELECT Count, Percent FROM OVERALL ORDER BY RecordAt DESC LIMIT 1; """
        cursor = self.conn.execute(q)
        records = [row for row in cursor]
        result = {
            "count": records[0][0],
            "percent": records[0][1]

        }
        return result
    ##################################  Get OVERALL ########################################


    ################################## Add New OVERALL ########################################
    def add_overall(self, record->dict)-> None:
        now = datetime.now()
        q = f"""INSERT INTO OVERALL VALUES(
            "{record['Count']}",
            "{record['Percent']}",
            {now}
        );"""
        self.conn.execute(q)
        self.conn.commit()
    ##################################  Add OVERALL ########################################



    ################################## User Lats Condition ########################################
    def user_condition(self, id-> int)-> str:
        q = f"""SELECT LastCommand FROM USERS WHERE ID=={id} """
        cursor = self.conn.execute(q)
        records = [row for row in cursor]
        return records[0][0]
    ################################## User Lats Condition ########################################


    ################################## User Lats Condition ########################################
    def update_user_condition(self, id-> int, condition-> str)-> None:
        q = f"""UPDATE USERS SET LastCommand = "{condition}" WHERE ID = {id} """
        self.conn.execute(q)
        self.conn.commit()


    ################################## User Lats Condition ########################################

    ################################## INSERT NEW Record #########################################
    def insert_record(self, record -> dict)-> None:
        now = datetime.now()
        self.disable(record["Symbol"])
        q = f"""INSERT INTO RECORDS VALUES(
            "{record['Symbol']}",
            "{record['FullName']}",
            {record['LastPrice']},
            {record['ClosedPrice']},
            {now},
            {record['Type']},
            True
        );"""
        self.conn.execute(q)
        self.conn.commit()

    ################################## INSERT NEW Record #########################################

    
    def closedb(self):
        self.conn.commit()
        self.conn.close()
        



def generator():
    db = Records()
    db.create()
    return db

if __name__ == "__main__":
    generator()

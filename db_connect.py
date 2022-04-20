import sqlite3
from datetime import datetime


class Records:
    def __init__(self):
        self.conn = sqlite3.connect('my_records.db')
        self.create()
    ########################## Create Table ######################################
    def create(self):
        records_table = """CREATE TABLE IF NOT EXISTS RECORDS(
            Symbol NVARCHAR,
            FullName  NVARCHAR(150),
            LastPrice NVARCHAR(50),
            ClosedPrice NVARCHAR(50),
            RecordAt DATETIME,
            Type INT,
            isLast BIT
        );"""
        over_all_table = """CREATE TABLE IF NOT EXISTS OVERALL(
            Count  NVARCHAR(100),
            Percent  NVARCHAR(100),
            RecordAt DATETIME
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
        q = f"""SELECT * FROM RECORDS WHERE isLast=TRUE;"""
        cursor = self.conn.execute(q)
        records = [row for row in cursor]
        return records
        
    ########################## GET LAST RECORDS #######################



    ################################## CHANGE isLAST STATUS ########################################
    def get_disable(self, symbol:str)-> None:
        q = f"""UPDATE RECORDS SET isLast = 0 WHERE Symbol = "{symbol}" """
        self.conn.execute(q)
        self.conn.commit()
    ################################## CHANGE iSLAST STATUS ########################################

    ################################## Get Symbol By Name ########################################
    def get_symbol(self, name:str)->str:
        q = f"""SELECT Symbol FROM RECORDS WHERE FullName ="{name}";"""
        cursor = self.conn.execute(q)
        records = [row for row in cursor]
        return records[0][0]
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
    def add_overall(self, record:dict)-> None:
        now = datetime.now()
        q = f"""INSERT INTO OVERALL VALUES("{record['Count']}", "{record['Percent']}", "{now}");"""
        self.conn.execute(q)
        self.conn.commit()
    ##################################  Add OVERALL ########################################



    ################################## User Lats Condition ########################################
    def user_condition(self, id:int)-> str:
        q = f"""SELECT LastCommand FROM USERS WHERE ID={id} """
        cursor = self.conn.execute(q)
        records = [row for row in cursor]
        return records[0][0]
    ################################## User Lats Condition ########################################

    ########################## Check Exicting User ##############################
    def user_exist(self, id:int)-> bool:
        q = f"""Select count(*) from USERS where ID = {id}"""
        count   =   self.conn.execute(q)
        for row in count:
            if row[0]>0:
                return  True
            else:
                return  False

    ########################## Check Exicting User ##############################


    ########################## Add New User ##############################
    def add_user(self, id:int):
        now = datetime.now()
        q = f"""INSERT INTO USERS VALUES({id}, "start", "{now}");"""
        self.conn.execute(q)
        self.conn.commit()
    ########################## Add New User ##############################



    ################################## User Lats Condition ########################################
    def update_user_condition(self, id:int, condition:str)-> None:
        q = f"""UPDATE USERS SET LastCommand = "{condition}" WHERE ID = {id} """
        self.conn.execute(q)
        self.conn.commit()


    ################################## User Lats Condition ########################################



    ################################## INSERT NEW Record #########################################
    def insert_record(self, record:dict)-> None:
        now = datetime.now()
        self.get_disable(record["Symbol"])
        q = f"""INSERT INTO RECORDS VALUES("{record['Symbol']}", "{record['FullName']}", "{record['LastPrice']}", "{record['ClosedPrice']}", "{now}", {record['Type']}, 1);"""
        self.conn.execute(q)
        self.conn.commit()

    ################################## INSERT NEW Record #########################################

    
    def closedb(self):
        self.conn.commit()
        self.conn.close()
        


class RecordManager:
    def __init__(self) -> None:
        self.db = Records()

    def get_last_records(self)->list:
        return self.db.get_records()

    def set_new_records(self, records:list):
        for record in records:
            self.db.insert_record(record)
        return True
    
    def get_last_command(self, user:object)-> str:
        if self.db.user_exist(user.id):
            result = self.db.user_condition(user.id)
            return result
        else:
            self.db.add_user(user.id)
            return "start"

    def set_last_command(self, user:object, condition:str)-> str:
        self.db.update_user_condition(user.id, condition)
        return True

    def get_last_overall(self):
        return self.db.get_overall()

    def set_overall(self, count:int, percent:int):
        self.db.add_overall({
            "Count":count,
            "Percent":percent
        })
        return True

    def get_symbol_by_name(self, name:str) ->str:
        response = self.db.get_symbol(name)
        return response

    def get_price_by_symbol(self, symbol:str)->dict:
        result = [record for record in self.get_last_records() if record[0] == symbol][0]
        return {
            "Symbol": result[0],
            "FullName": result[1],
            "LastPrice": result[2],
            "ClosedPrice": result[3]
        }

    def done(self):
        self.db.closedb()

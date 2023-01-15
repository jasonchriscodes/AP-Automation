import pyodbc

class DB():
    
    def __init__(self,dbType):
        self.dbType = dbType
        if(self.dbType=="SQLSERVER"):
            self.dbDriver = "{SQL Server}"
            #self.dbDriver = "{ODBC Driver 17 for SQL Server}"
            #self.dbDriver = DRIVER="{ODBC Driver 13 for SQL Server}"
        else:
            self.dbDriver = "{SQL Server}"
            #self.dbDriver = "{ODBC Driver 17 for SQL Server}"
            #self.dbDriver = DRIVER="{ODBC Driver 13 for SQL Server}"
    def getRowCount(self):
        return self.rowCount

    def connect(self,hostServer,db,dbUser,dbPassword):
        self.hostServer =hostServer
        self.db = db
        self.dbUser = dbUser
        self.dbPassword = dbPassword
        #print (hostServer)
        #print (db)
        #print(dbUser)
        #print(dbPassword)
        successConn = False
        try:
            print("Establishing db connection...")
            self.conn = pyodbc.connect(driver=self.dbDriver, host=hostServer, database=db,  user=dbUser, password=dbPassword,autocommit=True)
            #self.conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=cfaksql\ferret;DATABASE=FerretAP;UID=apautomation1;PWD=Office48')
            #self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=cfaksql\ferret;DATABASE=FerretAP;UID=apautomation1;PWD=Office48')
            #self.conn = pyodbc.connect('DSN=apautomation;Trusted_Connection=yes;')

            self.cursor = self.conn.cursor()
            print("Successfully connected to database.")
            successConn = True
        except Exception as e:
            print("Problem occurred in connecting to db server." + str(e))
        return successConn

    def setColumns(self,cols):
        self.cols = cols
        print(self.cols)

    def update(self,qry):
        self.cursor.execute(qry)
        self.rowCount = self.cursor.rowcount
        print("Number of rows effected:" + str(self.rowCount))
        self.conn.commit()

    def executeproc(self,qry):
        try:

            self.cursor.execute(qry)                   
            self.cursor.commit()
            #print(self.rows)
            print("Stored Proc executed successfully")
        except Exception as e:
            print("Exception occurred when executing stored proc : " + str(e))
    

    def execute(self,qry):
        try:

            self.cursor.execute(qry)                   
            self.rows = self.cursor.fetchall()
            #print(self.rows)
            print("Query executed successfully")            
            self.rowCount = len(self.rows)
            print("Number of rows found:" + str(self.rowCount))
            
        except Exception as e:
            print("Exception occurred when executing a query : " + str(e))
    
    def getRow(self,num):
        if(self.rowCount>num):
            #print("fetching row number:" + str(num))
            self.row = self.rows[num]
            #print(self.row)
        else:
            self.row = None
    
    def getValue(self,colName):
        val = str(self.row[self.cols[colName]])
        #print("Value:" + val)
        return val

    def close(self):
        try:
            self.cursor.close()
            del self.cursor
            self.conn.close()
            print("Successfully closed db connection.")
        except Exception as e:
            print("error occurred closing db connection:"+str(e))

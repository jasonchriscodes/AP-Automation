import pyodbc


#connString = 'Driver={SQL Server};Server=cfaksql\ferret;Database=FerretAP;UID=Apautomation;PWD=Office47;Trusted_Connection=yes;'
#conn = pyodbc.connect(connString)
server = 'cfaksql\\ferret'
db1='FerretAP'
tcon = 'yes'
uname = 'Apautomation'
pword='Office47'
#SQL Server Native Client 11.0
conn = pyodbc.connect(driver='{SQL Server}', host=server, database=db1,  user=uname, password=pword)
print(conn)
cursor = conn.cursor()
#cursor.execute("SELECT * FROM sys.tables")
#tables = cursor.fetchall()
cursor.execute("SELECT count(*) from PO_Ferret")
rows = cursor.fetchall()

for row in rows:
    print(row)
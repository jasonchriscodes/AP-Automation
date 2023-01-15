from lib.db import DB

db = DB("SQLSERVER")

dbhost = "cfaksql\\ferret"
dbname = "FerretAP"
dbuser = "Apautomation"
dbpass = "Office47"

if(db.connect(dbhost,dbname,dbuser,dbpass)):
    db.update("update tblDocument set DocStatusID='16' where DocID='1132'")
    db.close()
else:
    print("Connection error")    
import datetime

class Log:

    def __init__(self,path):
        self.lPath = path
        
    def add(self,msg):
        try:

            f =open(self.lPath,"a+")
            dt = datetime.datetime.now()
            now = dt.strftime("%c")
            f.write(now + ": " + msg+ "\n")
            print(now + ": " + msg)
            f.close()

        except Exception as e:
            print("Problem occured writing log to " + self.lPath)


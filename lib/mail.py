import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mailing:

    def __init__(self,type,useremail,password):
        if(type=="gmail"):
            self.s = smtplib.SMTP("smtp.gmail.com",465)
            self.s.starttls()
            self.s.login(useremail,password)
            self.msg = MIMEMultipart('alternative')
            self.msg['From'] = useremail

    def close(self):
        self.s.quit()
    
    def setSubject(self,sub):
        self.msg['Subject'] = sub

    def sendMail(self,type,you,carbCopy,text):
        #self.msg['To'] = you
        self.msg['To'] = you
        self.msg['Cc'] = carbCopy
        part = MIMEText(text, type)
        self.msg.attach(part)
        if(self.s.sendmail(self.msg['From'], [you,carbCopy], self.msg.as_string())):
            return 1
        else:
            return 0

    def sendPlainMail(self,you,carbCopy,text):
        self.sendMail('plain',you,carbCopy,text)

    def sendHTMLMail(self,you,carbCopy,text): 
        if(self.sendMail('html',you,carbCopy,text)):
            return 1
        else:
            return 0


from lib.mail import Mailing

m = Mailing("gmail","bpe.automation@gmail.com","wElcome@12345")
m.setSubject("Processing POs")
html = "<html><head></head><body>Hi Srinivas!<br/><br/>We are starting email processing now, please keep things <b>ready</b>.<br/><br/>Thank You,<br/>Regards,<br/>Srinivas P.</body></html>"
m.sendHTMLMail("srinivas.2447.p@gmail.com",html)
m.close()
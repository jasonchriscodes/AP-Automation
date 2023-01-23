from lib.mail import Mailing

m = Mailing("gmail","info@freightdesk.co.nz","Kecapasin23!")
m.setSubject("Processing POs")
html = "<html><head></head><body>Hi Srinivas!<br/><br/>We are starting email processing now, please keep things <b>ready</b>.<br/><br/>Thank You,<br/>Regards,<br/>Srinivas P.</body></html>"
m.sendHTMLMail("jasonchristian1234@gmail.com",html)
print("Your message has been sent.")
m.close()
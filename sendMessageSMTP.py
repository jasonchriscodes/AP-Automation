import os
from email.message import EmailMessage
import ssl
import smtplib
from email import errors

email_sender = 'info@demowebsites.co.nz'
email_password = 'Kecapasin23!'
email_receiver = 'jasonchristian1234@gmail.com'

subject = 'Email SMTP Centra Test'
body = """
Hi, test succeed
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('mail.demowebsites.co.nz', 465, context=context) as smtp:
 try:
  smtp.login(email_sender, email_password)
  smtp.sendmail(email_sender, email_receiver, em.as_string())
  print("Your message has been sent.")
 except errors.MessageError as error:
   print('An error occured: %s' % error)
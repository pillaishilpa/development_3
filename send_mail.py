import smtplib
SERVER = smtplib.SMTP(‘smtp.server.domain’)
FROM = sender@mail.com
TO = ["user@mail.com"] # must be a list
SUBJECT = "Hello!"
TEXT = "This message was sent with Python's smtplib."
# Main message
message = """
From: Sarah Naaz < sender@mail.com >
To: CarreerRide user@mail.com
Subject: SMTP email msg
This is a test email. Acknowledge the email by responding.
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, message)
server.quit()
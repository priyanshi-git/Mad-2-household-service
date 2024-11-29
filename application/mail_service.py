
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = "admin@iitm.ac.in"
SENDER_PASSOWRD = ""


def send_message(to, subject, content_body):
  msg = MIMEMultipart()
  msg['to']=to
  msg["subject"]=subject
  msg["from"]=SENDER_EMAIL
  msg.attach(MIMEText(content_body, 'html'))
  client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
  client.send_message(msg=msg)
  client.quit()
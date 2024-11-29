from celery import shared_task
from .mail_service import send_message

@shared_task(ignore_result=True)
def daily_reminder(to, subject):
  send_message(to, subject, "hello")
  return "OK"
  
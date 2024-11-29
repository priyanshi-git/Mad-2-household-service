from celery import shared_task

@shared_task(ignore_result=False)
def daily_reminder(message):
  return message
  
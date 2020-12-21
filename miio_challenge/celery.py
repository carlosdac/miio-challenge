
from sendgrid import SendGridAPIClient
from django.conf import settings
from sendgrid.helpers.mail import Mail
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miio_challenge.settings')

app = Celery('miio_challenge', broker='redis://0.0.0.0:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task()
def send_mail(user):
  message = Mail(
  from_email='test@miiotest.com',
  to_emails=user['email'],
  subject='You registered a Regular Plan',
  html_content='Hi ' + user['first_name'] + '! Your Regular Plan was registred with success.')
  try:
      sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
      response_email = sg.send(message)
      print(response_email.status_code)
  except Exception as e:
      print(e.message)
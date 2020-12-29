
from sendgrid import SendGridAPIClient
from django.conf import settings
from sendgrid.helpers.mail import Mail
import os
from pymongo import MongoClient 
from celery import Celery
import urllib.parse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miio_challenge.settings')

app = Celery('miio_challenge', broker=settings.REDIS_URL)

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
      return sg.send(message)
  except Exception as e:
      print(str(e))





@app.task()
def save_mongodb(document, collection_name):
    username = urllib.parse.quote_plus(settings.MONGODB_USER)
    password = urllib.parse.quote_plus(settings.MONGODB_PASSWORD)
    mongo_client = MongoClient(settings.MONGODB_URL % (username, password)) 
    mongo_database = mongo_client[settings.MONGODB_DB]
    collection = mongo_database[collection_name]
    return collection.insert_one(document).inserted_id
    


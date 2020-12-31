
from sendgrid import SendGridAPIClient
from django.conf import settings
from sendgrid.helpers.mail import Mail
import os
from pymongo import MongoClient 
from celery import Celery
import urllib.parse

get_env = os.environ.get
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miio_challenge.settings')

print("redis://", get_env('REDIS_HOST'), ":", get_env('REDIS_PORT') , '/' , get_env('REDIS_DB'))
app = Celery('miio_challenge', broker="redis://" + get_env('REDIS_HOST') + ":" + get_env('REDIS_PORT') + '/' + get_env('REDIS_DB'))
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
      sg = SendGridAPIClient(get_env('SENDGRID_API_KEY'))
      return sg.send(message)
  except Exception as e:
      print(str(e))





@app.task()
def save_mongodb(document, collection_name):
    username = urllib.parse.quote_plus(get_env('MONGODB_USER'))
    password = urllib.parse.quote_plus(get_env('MONGODB_PASSWORD'))
    mongo_client = MongoClient("mongodb://%s:%s@%s:%s" % (username, password, get_env('MONGODB_HOST'), get_env('MONGODB_PORT'))) 
    mongo_database = mongo_client[get_env('MONGODB_DB')]
    collection = mongo_database[collection_name]
    return collection.insert_one(document).inserted_id
    


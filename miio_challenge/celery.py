
from sendgrid import SendGridAPIClient
from django.conf import settings
from sendgrid.helpers.mail import Mail
import os
from pymongo import MongoClient 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miio_challenge.settings')

app = Celery('miio_challenge', broker=settings.REDIS_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task()
def send_mail(user):
#   message = Mail(
#   from_email='test@miiotest.com',
#   to_emails=user['email'],
#   subject='You registered a Regular Plan',
#   html_content='Hi ' + user['first_name'] + '! Your Regular Plan was registred with success.')
#   try:
#       sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
#       response_email = sg.send(message)
#     #   print(response_email.status_code)
#   except Exception as e:
#       print(e.message)
    pass


import urllib.parse

username = urllib.parse.quote_plus(settings.MONGODB_USER)
password = urllib.parse.quote_plus(settings.MONGODB_PASSWORD)


@app.task()
def save_mongodb(document, collection_name):
    mongo_client = MongoClient(settings.MONGODB_URL % (username, password)) 
    print(settings.MONGODB_URL % (username, password))
    mongo_database = mongo_client[settings.MONGODB_DB]
    collection = mongo_database[collection_name]
    id = collection.insert_one(document).inserted_id
    # print(id)


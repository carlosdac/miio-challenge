from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIClient,APITestCase
from .models import RegularPlan
from unittest.mock import Mock
from miio_challenge.celery import send_mail, save_mongodb
from django.contrib.auth.models import User
import urllib.parse
from pymongo import MongoClient 
from django.conf import settings
import json
from .serializers import *
# Create your tests here.

class RegularPlanCreateTestCase(APITestCase):
  def setUp(self, *args, **kwargs):
    self.client = APIClient()
    self.response_content_expected = {
      "id": 2,
      "owner": {
        "first_name": "Carlos",
        "last_name": "Daniel",
        "username": "one",
        "id": 5,
        "email": "mano@gmai.com",
        },
      "name": "My Regular Plan",
      "tar_included": True,
      "subscription": 1.0,
      "cycle": 1,
      "type": 2,
      "offer_iva": False,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "valid": False,
      "publish": False,
      "vat": 100
    }
    self.data = {
      "name": "My Regular Plan",
      "subscription": 1,
      "cycle": 1,
      "type": 2,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "publish": False,
      "valid": False,
      "offer_iva": False,
      "tar_included": True,
      "vat": 100,
    }
    user= {
      "first_name": "Carlos",
      "last_name": "Daniel",
      "username": "one",
      "password": "ds",
      "email": "mano@gmai.com",
    }

    url = reverse('register')
    self.user_one  = self.client.post(url, user ,format='json')

    url = reverse('login')
    self.user_one = self.client.post(url, {"username": user['username'], "password": user['password']} ,format='json')

    user['username'] = "two"
    url = reverse('register')
    self.user_two  = self.client.post(url, user ,format='json')
    
    url = reverse('login')
    self.user_two = self.client.post(url, {"username": user['username'], "password": user['password']} ,format='json')


    self.url = reverse('create or list')
    return super(RegularPlanCreateTestCase, self).setUp(*args, **kwargs)

  def test_registration_regular_plan_success(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    response  = self.client.post(self.url, self.data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(name=self.data['name']).count(), 1)

  def test_registration_regular_plan_without_user_authenticated(self):  
    response  = self.client.post(self.url, self.data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_without_name(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['name']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"name": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_without_name_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    data['name'] = ""
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"name": ["This field may not be blank."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_name_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    data['name'] = "My Regular Plan of 2020"
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(name=data['name']).count(), 1)

  def test_registration_regular_plan_without_tar_included(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['tar_included']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"tar_included": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_tar_included_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    data['tar_included'] = True
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(tar_included=data['tar_included']).count(), 1)


    data['tar_included'] = False
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(tar_included=data['tar_included']).count(), 1)


  def test_registration_regular_plan_without_subscription(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['subscription']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"subscription": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_without_subscription_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['subscription'] = -1
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"subscription": ["-1.0 is not bigger than zero."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data['subscription'] = 0
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"subscription": ["0.0 is not bigger than zero."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data['subscription'] = "Test"
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"subscription": ["A valid number is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)
  
  def test_registration_regular_plan_with_subscription_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['subscription'] = 0.01
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(subscription=data['subscription']).count(), 1)

  def test_registration_regular_plan_without_cycle(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['cycle']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"cycle": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_without_cycle_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    data['cycle'] = 10
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"cycle": ['"10" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data['cycle'] = -1
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"cycle": ['"-1" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data['cycle'] = "Test"
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"cycle": ['"Test" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_cycle_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['cycle'] = 1
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(cycle=data['cycle']).count(), 1)

    data['cycle'] = 2
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(cycle=data['cycle']).count(), 1)

  def test_registration_regular_plan_without_type(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['type']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"type": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_without_type_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    data['type'] = 10
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {'type': ['"10" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data['type'] = -1
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"type": ['"-1" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data['type'] = "Test"
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"type": ['"Test" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_type_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['type'] = 1
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(type=data['type']).count(), 1)

    data['type'] = 2
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(type=data['type']).count(), 1)

    data['type'] = 3
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(type=data['type']).count(), 1)

  def test_registration_regular_plan_without_offer_iva(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['offer_iva']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"offer_iva": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_offer_iva_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['offer_iva'] = True
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(offer_iva=data['offer_iva']).count(), 1)

    data['offer_iva'] = False
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(offer_iva=data['offer_iva']).count(), 1)


  def test_registration_regular_plan_without_off_peak_price(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['off_peak_price']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {'off_peak_price': ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_without_off_peak_price_valid(self):
    field = 'off_peak_price'
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data[field] = -1
    response  = self.client.post(self.url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {field: ['-1.0 is not bigger than zero.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data[field] = 0
    response  = self.client.post(self.url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {field: ['0.0 is not bigger than zero.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data[field] = "Test"
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {field: ['A valid number is required.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_off_peak_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['off_peak_price'] = 0.01
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(off_peak_price=data['off_peak_price']).count(), 1)

  def test_registration_regular_plan_without_peak_price(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['peak_price']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {'peak_price': ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)


  def test_registration_regular_plan_without_peak_price_valid(self):
    field = 'peak_price'
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data[field] = -1
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {field: ['-1.0 is not bigger than zero.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data[field] = 0
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {field: ['0.0 is not bigger than zero.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data[field] = "Test"
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {field: ['A valid number is required.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)


  def test_registration_regular_plan_with_peak_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['peak_price'] = 0.01
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(peak_price=data['peak_price']).count(), 1)


  def test_registration_regular_plan_without_unit(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['unit']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"unit": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)


  def test_registration_regular_plan_without_unit_valid(self):
    field = 'unit'
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    data[field] = 10
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {field: ['"10" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data[field] = -1
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {field: ['"-1" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

    data[field] = "Test"
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {field: ['"Test" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_unit_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['unit'] = 1
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(unit=data['unit']).count(), 1)

    data['unit'] = 2
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(unit=data['unit']).count(), 1)


  def test_registration_regular_plan_without_field_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['valid']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"valid": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_field_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['valid'] = True
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(valid=data['valid']).count(), 1)

    data['valid'] = False
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(valid=data['valid']).count(), 1)



  def test_registration_regular_plan_without_publish(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['publish']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"publish": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_publish_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['publish'] = False
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(RegularPlan.objects.filter(publish=data['publish']).count(), 1)

  def test_registration_regular_plan_without_publish_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data

    data['publish'] = True
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(RegularPlan.objects.filter(publish=data['publish']).count(), 0)


  def test_registration_regular_plan_without_vat(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    del data['vat']
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"vat": ["This field is required."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_vat_less_than_one(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    data['vat'] = -1
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"vat": ["Ensure this value is greater than or equal to 1."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_vat_bigger_then_hundred(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    data['vat'] = 101
    response  = self.client.post(self.url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"vat": ["Ensure this value is less than or equal to 100."]})
    self.assertEqual(RegularPlan.objects.filter().count(), 0)

  def test_registration_regular_plan_with_vat_equal_hundred(self):
    response_content_expected = self.response_content_expected
    del response_content_expected['id']
    del response_content_expected['owner']['id']
    response_content_expected['vat'] = 100
    
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    data = self.data
    data['vat'] = 100
    
    response  = self.client.post(self.url, data, format='json')
    response_content = json.loads(response.content)
    del response_content['id']
    del response_content['owner']['id']
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response_content, response_content_expected)
    self.assertEqual(RegularPlan.objects.filter().count(), 1)
  
  def test_registration_regular_plan_with_subscription_more_than_zero(self):
    response_content_expected = self.response_content_expected
    del response_content_expected['id']
    del response_content_expected['owner']['id']
    response_content_expected['subscription'] = 0.01
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    
    data = self.data
    data['subscription'] = 0.01
    response  = self.client.post(self.url, data, format='json')
    response_content = json.loads(response.content)
    del response_content['id']
    del response_content['owner']['id']
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response_content, response_content_expected)
    self.assertEqual(RegularPlan.objects.filter().count(), 1)


class RegularPlanUpdateTestCase(APITestCase):
  def setUp(self, *args, **kwargs):
    self.client = APIClient()
    self.response_content_expected = {
      "id": 2,
      "owner": {
        "first_name": "Carlos",
        "last_name": "Daniel",
        "username": "one",
        "id": 5,
        "email": "mano@gmai.com",
        },
      "name": "My Regular Plan",
      "tar_included": True,
      "subscription": 1.0,
      "cycle": 1,
      "type": 2,
      "offer_iva": False,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "valid": False,
      "publish": False,
      "vat": 100
    }
    self.data = {
      "name": "My Regular Plan",
      "subscription": 1,
      "cycle": 1,
      "type": 2,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "publish": False,
      "valid": False,
      "offer_iva": False,
      "tar_included": True,
      "vat": 100,
    }
    user= {
      "first_name": "Carlos",
      "last_name": "Daniel",
      "username": "one",
      "password": "ds",
      "email": "mano@gmai.com",
    }

    url = reverse('register')
    self.user_one  = self.client.post(url, user ,format='json')

    url = reverse('login')
    self.user_one = self.client.post(url, {"username": user['username'], "password": user['password']} ,format='json')

    user['username'] = "two"
    url = reverse('register')
    self.user_two  = self.client.post(url, user ,format='json')
    
    url = reverse('login')
    self.user_two = self.client.post(url, {"username": user['username'], "password": user['password']} ,format='json')


    return super(RegularPlanUpdateTestCase, self).setUp(*args, **kwargs)
  
  
  def test_update_name_regular_plan_with_all_attrs_success(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})  
    
    data['name'] = "New Regular Plan name"
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content)['name'], data['name'])
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], name=data['name']).count(), 1)

  def test_update_regular_plan_without_user_authenticated(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})  

    self.client.credentials(HTTP_AUTHORIZATION="")
    response  = self.client.patch(url, data, format='json') 
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id']).count(), 1)

  def test_update_regular_plan_with_owner_diff_of_user_authenticated(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})  

    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_two.data['token'])
    response  = self.client.patch(url, data, format='json') 
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id']).count(), 1)

  def test_update_regular_plan_without_name(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['name']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter().count(), 1)
  
  def test_update_regular_plan_without_name_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    data['name'] = ""
    response  = self.client.patch(url, data, format='json')


    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"name": ["This field may not be blank."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'],name=self.data['name']).count(), 1)

  def test_update_regular_plan_with_name(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['name'] = "Alter name"
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], name=response_content['name']).count(), 1)

  def test_update_regular_plan_without_tar_included(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['tar_included']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], tar_included=self.data['tar_included']).count(), 1)
  

  def test_update_regular_plan_with_tar_included(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['tar_included'] = True
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], tar_included=response_content['tar_included']).count(), 1)

    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['tar_included'] = False
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], tar_included=response_content['tar_included']).count(), 1)

  def test_update_regular_plan_without_subscription(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['subscription']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], subscription=self.data['subscription']).count(), 1)

  def test_update_regular_plan_without_subscription_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)

    url = reverse("update", kwargs={"pk": response_content['id']})
    
    data['subscription'] = -1
    response  = self.client.patch(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"subscription": ["-1.0 is not bigger than zero."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], subscription=self.data['subscription']).count(), 1)
    
    data['subscription'] = 0
    response  = self.client.patch(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"subscription": ["0.0 is not bigger than zero."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], subscription=self.data['subscription']).count(), 1)
    
    data['subscription'] = "Test"
    response  = self.client.patch(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"subscription": ["A valid number is required."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], subscription=self.data['subscription']).count(), 1)

  def test_update_regular_plan_with_subscription_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['subscription'] = 29.90
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], subscription=response_content['subscription']).count(), 1)
  
  def test_update_regular_plan_without_cycle(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['cycle']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], cycle=self.data['cycle']).count(), 1)

  def test_update_regular_plan_without_cycle_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)

    url = reverse("update", kwargs={"pk": response_content['id']})

    data['cycle'] = 10
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"cycle": ['"10" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], cycle=self.data['cycle']).count(), 1)

    data['cycle'] = -1
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"cycle": ['"-1" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], cycle=self.data['cycle']).count(), 1)

    data['cycle'] = "Test"
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"cycle": ['"Test" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], cycle=self.data['cycle']).count(), 1)

  def test_update_regular_plan_with_cycle_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['cycle'] = 1
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], cycle=response_content['cycle']).count(), 1)

    response_content['cycle'] = 2
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], cycle=response_content['cycle']).count(), 1)

  def test_update_regular_plan_without_type(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['type']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], type=self.data['type']).count(), 1)

  def test_update_regular_plan_without_type_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)

    url = reverse("update", kwargs={"pk": response_content['id']})

    data['type'] = 10
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"type": ['"10" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], type=self.data['type']).count(), 1)

    data['type'] = -1
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"type": ['"-1" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], type=self.data['type']).count(), 1)

    data['type'] = "Test"
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"type": ['"Test" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], type=self.data['type']).count(), 1)
  
  def test_update_regular_plan_with_type_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['type'] = 1
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], type=response_content['type']).count(), 1)

    response_content['type'] = 2
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], type=response_content['type']).count(), 1)


    response_content['type'] = 3
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], type=response_content['type']).count(), 1)

  def test_update_regular_plan_without_offer_iva(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['offer_iva']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], offer_iva=self.data['offer_iva']).count(), 1)

  def test_update_regular_plan_with_offer_iva_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['offer_iva'] = True
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], offer_iva=response_content['offer_iva']).count(), 1)

    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['offer_iva'] = False
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], offer_iva=response_content['offer_iva']).count(), 1)

  def test_update_regular_plan_without_off_peak_price(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['off_peak_price']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], off_peak_price=self.data['off_peak_price']).count(), 1)

  def test_update_regular_plan_without_off_peak_price_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)

    url = reverse("update", kwargs={"pk": response_content['id']})
    
    data['off_peak_price'] = -1
    response  = self.client.patch(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"off_peak_price": ["-1.0 is not bigger than zero."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], off_peak_price=self.data['off_peak_price']).count(), 1)
    
    data['off_peak_price'] = 0
    response  = self.client.patch(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"off_peak_price": ["0.0 is not bigger than zero."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], off_peak_price=self.data['off_peak_price']).count(), 1)
    
    data['off_peak_price'] = "Test"
    response  = self.client.patch(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"off_peak_price": ["A valid number is required."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], off_peak_price=self.data['off_peak_price']).count(), 1)

  def test_update_regular_plan_with_off_peak_price_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['off_peak_price'] = 0.06
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], off_peak_price=response_content['off_peak_price']).count(), 1)

  def test_update_regular_plan_without_peak_price(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['peak_price']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], peak_price=self.data['peak_price']).count(), 1)

  def test_update_regular_plan_without_peak_price_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)

    url = reverse("update", kwargs={"pk": response_content['id']})
    
    data['peak_price'] = -1
    response  = self.client.patch(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"peak_price": ["-1.0 is not bigger than zero."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], peak_price=self.data['peak_price']).count(), 1)
    
    data['peak_price'] = 0
    response  = self.client.patch(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"peak_price": ["0.0 is not bigger than zero."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], peak_price=self.data['peak_price']).count(), 1)
    
    data['peak_price'] = "Test"
    response  = self.client.patch(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"peak_price": ["A valid number is required."]})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], peak_price=self.data['peak_price']).count(), 1)

  def test_update_regular_plan_with_peak_price_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['peak_price'] = 0.06
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], peak_price=response_content['peak_price']).count(), 1)

  def test_update_regular_plan_without_unit(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['unit']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], unit=self.data['unit']).count(), 1)

  def test_update_regular_plan_without_unit_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)

    url = reverse("update", kwargs={"pk": response_content['id']})

    data['unit'] = 10
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"unit": ['"10" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], unit=self.data['unit']).count(), 1)

    data['unit'] = -1
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"unit": ['"-1" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], unit=self.data['unit']).count(), 1)

    data['unit'] = "Test"
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(json.loads(response.content), {"unit": ['"Test" is not a valid choice.']})
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], unit=self.data['unit']).count(), 1)

  def test_update_regular_plan_with_unit_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['unit'] = 1
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], unit=response_content['unit']).count(), 1)

    response_content['unit'] = 2
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], unit=response_content['unit']).count(), 1)

  def test_update_regular_plan_without_field_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['valid']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], valid=self.data['valid']).count(), 1)   
  
  def test_update_regular_plan_with_field_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['valid'] = True
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], valid=response_content['valid']).count(), 1)

    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['valid'] = False
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], valid=response_content['valid']).count(), 1)

  def test_update_regular_plan_without_publish(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['publish']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], publish=self.data['publish']).count(), 1)   

  def test_update_regular_plan_with_publish_valid(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['publish'] = True
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], publish=response_content['publish']).count(), 1)

    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['publish'] = False
    response  = self.client.patch(url, response_content, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], publish=response_content['publish']).count(), 1)

  def test_update_regular_plan_without_vat(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    del data['vat']
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(json.loads(response.content), response_content)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], vat=self.data['vat']).count(), 1)

  def test_update_regular_plan_with_vat_less_than_one(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    data['vat'] = -1
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], vat=self.data['vat']).count(), 1)
    self.assertEqual(json.loads(response.content), {"vat": ["Ensure this value is greater than or equal to 1."]})

  def test_update_regular_plan_with_vat_bigger_then_hundred(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    data['vat'] = 101
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], vat=self.data['vat']).count(), 1)
    self.assertEqual(json.loads(response.content), {"vat": ["Ensure this value is less than or equal to 100."]})

  def test_update_regular_plan_with_vat_equal_hundred(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['vat'] = 100
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], vat=response_content['vat']).count(), 1)
    self.assertEqual(json.loads(response.content), response_content)
    
  def test_update_regular_plan_with_subscription_more_than_zero(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    
    url = reverse("update", kwargs={"pk": response_content['id']})
    response_content['vat'] = 100
    response  = self.client.patch(url, data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(RegularPlan.objects.filter(id=response_content['id'], vat=response_content['vat']).count(), 1)
    self.assertEqual(json.loads(response.content), response_content)

class RegularPlanGetTestCase(APITestCase):
  def setUp(self, *args, **kwargs):
    self.client = APIClient()
    self.data = {
      "name": "My Regular Plan",
      "subscription": 1.0,
      "cycle": 1,
      "type": 2,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "publish": False,
      "valid": False,
      "offer_iva": False,
      "tar_included": True,
      "vat": 100,
    }
    user= {
      "first_name": "Carlos",
      "last_name": "Daniel",
      "username": "one",
      "password": "ds",
      "email": "mano@gmai.com",
    }

    url = reverse('register')
    self.user_one  = self.client.post(url, user ,format='json')

    url = reverse('login')
    self.user_one = self.client.post(url, {"username": user['username'], "password": user['password']} ,format='json')

    user['username'] = "two"
    url = reverse('register')
    self.user_two  = self.client.post(url, user ,format='json')
    
    url = reverse('login')
    self.user_two = self.client.post(url, {"username": user['username'], "password": user['password']} ,format='json')


    self.url = reverse('create or list')
    return super(RegularPlanGetTestCase, self).setUp(*args, **kwargs)

  def test_list_regular_plan_with_success_and_publish_true(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')


    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_two.data['token'])
    
    url = reverse('create or list')    
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')

    response  = self.client.get(self.url + '?publish=True', format='json')
    response_content = json.loads(response.content)
    
    self.assertEquals(response.status_code, status.HTTP_200_OK)
    self.assertEquals(len(response_content['results']), 4)
  
  def test_list_regular_plan_with_user_not_authenticated_and_publish_true(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')


    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_two.data['token'])
    
    url = reverse('create or list')    
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')

    self.client.credentials(HTTP_AUTHORIZATION="")
    response  = self.client.get(self.url + '?publish=True', format='json')
    response_content = json.loads(response.content)
    
    self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEquals(response_content, {"detail": "Authentication credentials were not provided."})
  
  def test_list_regular_plan_with_success_user_not_authenticated(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')


    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_two.data['token'])
    
    url = reverse('create or list')    
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')

    self.client.credentials(HTTP_AUTHORIZATION="")
    response  = self.client.get(self.url, format='json')
    response_content = json.loads(response.content)
    
    self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEquals(response_content, {"detail": "Authentication credentials were not provided."})
  
  def test_list_regular_plan_with_success_user_authenticated(self):
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')


    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_two.data['token'])
    
    url = reverse('create or list')    
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    
    url = reverse('create or list')
    data = dict(self.data)
    response  = self.client.post(url, data, format='json')
    response_content = json.loads(response.content)
    url = reverse("update", kwargs={"pk": response_content['id']})  
    data['publish'] = True
    self.client.patch(url, data, format='json')


    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_one.data['token'])
    response  = self.client.get(self.url, format='json')
    response_content = json.loads(response.content)
    
    self.assertEquals(response.status_code, status.HTTP_200_OK)
    self.assertEquals(len(response_content['results']), 2)

class RegularPlanTasksTestCase(APITestCase):

  def setUp(self, *args, **kwargs):
    self.client = APIClient()
    self.user= {
      "first_name": "Carlos",
      "last_name": "Daniel",
      "username": "one",
      "password": "teste",
      "email": "carlosd.1199@gmail.com",
    }
    return super(RegularPlanTasksTestCase, self).setUp(*args, **kwargs)



  def test_send_mail(self):
    send_mail = Mock()
    send_mail(self.user)
    send_mail.assert_called_once_with(self.user)
  
  def test_save_mongodb(self):
    url = reverse('register')
    user  = json.loads(self.client.post(url, self.user ,format='json').content)


    data = {
      "name": "My Regular Plan",
      "subscription": 1,
      "cycle": 1,
      "type": 2,
      "off_peak_price": 0.05,
      "peak_price": 2.23,
      "unit": 1,
      "publish": False,
      "valid": False,
      "offer_iva": False,
      "tar_included": True,
      "vat": 100,
      "owner_id": user['id']
    }
    

    serializer = RegularPlanSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    regular_plan_created = serializer.save()
    regular_plan_created_serializer = RegularPlanSerializer(regular_plan_created)

    username = urllib.parse.quote_plus(settings.MONGODB_USER)
    password = urllib.parse.quote_plus(settings.MONGODB_PASSWORD)
    
    mongo_client = MongoClient(settings.MONGODB_URL % (username, password)) 
    mongo_database = mongo_client[settings.MONGODB_DB]
    collection = mongo_database['regularPlans']

    save_mongodb = Mock()
    save_mongodb(regular_plan_created_serializer.data, 'regularPlans')

    document_saved = collection.find_one({"id": regular_plan_created_serializer.data['id']})

    save_mongodb.assert_called_with(regular_plan_created_serializer.data, 'regularPlans')
    self.assertNotEqual(document_saved, None)

    

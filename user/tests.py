import json
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
##

from django.contrib.auth.models import User

import json
# Create your tests here.

class UserTestCase(APITestCase):
  def setUp(self):
    self.client = APIClient()
    user = User.objects.create(
      username="chiquinho",
      first_name="Francisco",
      last_name="chagas",
      email="mail@mail.com"
    )
    user.set_password("teste2")
    user.save()

  def test_login_user_existing(self):
    url = reverse('login')
    data = {
      "username": "chiquinho",
      "password": "teste2"
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)


  def test_login_user_not_existing(self):
    url = reverse('login')
    data = {
      "username": "chiquin",
      "password": "teste2"
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(json.loads(response.content), {"non_field_errors": ["Unable to log in with provided credentials."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_login_without_user(self):
    url = reverse('login')
    data = {
      "password": "teste2"
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(json.loads(response.content), {"username": ["This field is required."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


  def test_login_without_password(self):
    url = reverse('login')
    data = {
      "username": "teste2"
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(json.loads(response.content), {"password": ["This field is required."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_login_user_with_password_incorrect(self):
    url = reverse('login')
    data = {
      "username": "chiquinho",
      "password": "testeeew"
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(json.loads(response.content), {"non_field_errors": ["Unable to log in with provided credentials."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_registration_user_success(self):
    url = reverse('register')
    data = {
    "first_name": "Carlos",
    "last_name": "Daniel",
    "username": "manofsc",
    "password": "ds",
    "email": "mano@gmai.com",
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    user_exists = User.objects.filter(username="manofsc").exists()
    self.assertEqual(user_exists, True)

  def test_registration_user_with_username_existing(self):
    url = reverse('register')
    data = {
    "first_name": "Carlos",
    "last_name": "Daniel",
    "username": "chicó",
    "password": "ds",
    "email": "mano@gmai.com",
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    response  = self.client.post(url, data ,format='json')
    self.assertEqual(json.loads(response.content), {"username": ["A user with that username already exists."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    user_count = User.objects.filter(username="chicó").count()
    self.assertEqual(user_count, 1)

  def test_registration_user_without_username(self):
    url = reverse('register')
    data = {
    "first_name": "Carlos",
    "last_name": "Daniel",
    "password": "ds",
    "email": "mano@gmai.com",
    }
    response  = self.client.post(url, data ,format='json')    
    self.assertEqual(json.loads(response.content), {"username": ["This field is required."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_registration_user_without_email(self):
    url = reverse('register')
    data = {
    "first_name": "Carlos",
    "last_name": "Daniel",
    "username": "chiquinho234",
    "password": "ds",
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(json.loads(response.content), {"email": ["This field is required."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


  def test_registration_user_without_password(self):
    url = reverse('register')
    data = {
    "first_name": "Carlos",
    "last_name": "Daniel",
    "username": "chiquinho2345",
    "email": "mano@gmai.com",
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(json.loads(response.content), {"password": ["This field is required."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


  def test_registration_user_without_first_name(self):
    url = reverse('register')
    data = {
    "last_name": "Daniel",
    "username": "chiquinho2345",
    "password": "marcos",
    "email": "mano@gmai.com",
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(json.loads(response.content), {"first_name": ["This field is required."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_registration_user_without_last_name(self):
    url = reverse('register')
    data = {
    "first_name": "Daniel",
    "username": "chiquinho11212",
    "password": "marcos",
    "email": "mano@gmai.com",
    }
    response  = self.client.post(url, data ,format='json')
    self.assertEqual(json.loads(response.content), {"last_name": ["This field is required."]})
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

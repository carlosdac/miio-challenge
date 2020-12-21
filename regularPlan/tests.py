from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
##

from django.contrib.auth.models import User


# from .utils import generate_token_to_user

import json
# Create your tests here.

class RegularPlanCreateTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()

    return super().setUp()

  def test_registration_regular_plan_success(self):
    pass

  def test_registration_regular_plan_without_user_authenticated(self):
    pass

  def test_registration_regular_plan_without_name(self):
    pass
  
  def test_registration_regular_plan_without_name_valid(self):
    pass

  def test_registration_regular_plan_without_tar_included(self):
    pass

  def test_registration_regular_plan_without_subscription(self):
    pass

  def test_registration_regular_plan_without_subscription_valid(self):
    pass

  def test_registration_regular_plan_without_cycle(self):
    pass

  def test_registration_regular_plan_without_cycle_valid(self):
    pass

  def test_registration_regular_plan_without_type(self):
    pass

  def test_registration_regular_plan_without_type_valid(self):
    pass

  def test_registration_regular_plan_without_offer_iva(self):
    pass

  def test_registration_regular_plan_without_off_peak_price(self):
    pass

  def test_registration_regular_plan_without_off_peak_price_valid(self):
    pass

  def test_registration_regular_plan_without_peak_price(self):
    pass


  def test_registration_regular_plan_without_peak_price_valid(self):
    pass

  def test_registration_regular_plan_without_unit(self):
    pass


  def test_registration_regular_plan_without_valid(self):
    pass

  def test_registration_regular_plan_without_unit_valid(self):
    pass

  def test_registration_regular_plan_without_publish(self):
    pass

  def test_registration_regular_plan_without_vat(self):
    pass

  def test_registration_regular_plan_with_vat_less_than_one(self):
    pass

  def test_registration_regular_plan_with_vat_bigger_then_hundred(self):
    pass

  def test_registration_regular_plan_without_owner(self):
    pass


class RegularPlanPutTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()

    return super().setUp()

class RegularGetTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()

    return super().setUp()
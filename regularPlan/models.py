from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.

def validate_bigger_than_zero(value):
  if value <= 0:
    raise ValidationError(
    _('%(value)s is not bigger than zero'),
    params={'value': value},
    )


class RegularPlan(models.Model):

  Unit_types = models.IntegerChoices('UnitType', 'kwh min')
  Cycle_types = models.IntegerChoices('CycleType',  'daily weekly')
  Tariff_types = models.IntegerChoices('TariffType','bi-time tri-time simple')

  name = models.CharField(max_length=100, null=False, blank=False)
  tar_included = models.BooleanField()
  subscription = models.FloatField(null=False, blank=False, validators=[validate_bigger_than_zero])
  cycle = models.IntegerField(null=False, blank=False, choices=Cycle_types.choices)
  type = models.IntegerField(null=False, blank=False, choices=Tariff_types.choices)
  offer_iva = models.BooleanField()
  off_peak_price = models.FloatField(null=False, blank=False, validators=[validate_bigger_than_zero])
  peak_price = models.FloatField(null=False, blank=False, validators=[validate_bigger_than_zero])
  unit = models.IntegerField(null=False, blank=False, choices=Unit_types.choices)
  valid = models.BooleanField()
  publish = models.BooleanField()
  vat = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

  owner = models.ForeignKey(User,null=True, on_delete=models.SET_NULL, blank=True)
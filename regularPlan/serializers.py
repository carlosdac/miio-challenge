from .models import RegularPlan
from rest_framework import serializers
from user.serializers import UserSerializer
from django.contrib.auth.models import User
from miio_challenge.celery import send_mail

"""
This class implements a Serializer from Regular Plan model and overrides an methods create and save from ModelSerializer to
verify the value from publish in create and send mail in save, if publish is true.
"""
class RegularPlanSerializer(serializers.ModelSerializer):
  owner = UserSerializer(many=False, read_only=True)
  owner_id = serializers.PrimaryKeyRelatedField(many=False, required=False, write_only=True, queryset=User.objects.all().values_list('id', flat=True))

  class Meta:
    model = RegularPlan
    fields = "__all__"
    extra_kwargs = {'id': {'read_only': True}}
  
  def create(self, *args, **kwargs):
    if self.validated_data['publish']:
      raise serializers.ValidationError({
      "publish": [
        "This field can not true if you be creating a Regular Plan."
      ]
    })
    return super(RegularPlanSerializer, self).create(*args, **kwargs)

  def save(self, *args, **kwargs):
    value = super(RegularPlanSerializer, self).save(*args, **kwargs)
    if value.publish:
      user_serializer = UserSerializer(value.owner)
      send_mail(user_serializer.data)
    return value

from .models import RegularPlan
from rest_framework import serializers
from user.serializers import UserSerializer
from django.contrib.auth.models import User

class RegularPlanSerializer(serializers.ModelSerializer):
  owner = UserSerializer(many=False, read_only=True)
  owner_id = serializers.PrimaryKeyRelatedField(many=False, write_only=True, queryset=User.objects.all().values_list('id', flat=True))

  class Meta:
    model = RegularPlan
    fields = "__all__"
    extra_kwargs = {'id': {'read_only': True}}
from django.contrib.auth.models import User
from rest_framework import serializers


"""
This class implements a Serializer from User Django model and overrides a method create from ModelSerializer to
use method set_password from User model and have not problems with hash.
"""
class UserSerializer (serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ['id', 'password', 'username', 'first_name', 'last_name', 'email']
    extra_kwargs = {
      'password': {
          'required': True,
          'write_only': True
      },
      'email': {
          'required': True
      },
      'first_name': {
          'required': True
      },
      
      'last_name': {
          'required': True
      },
      'id': {
          'read_only': True
      }
    }

  def create(self, validated_data=None):
    user = User(
      username=self.validated_data['username'],
      email=self.validated_data['email'],
      first_name=self.validated_data['first_name'],
      last_name=self.validated_data['last_name']
    )
    user.set_password(self.validated_data['password'])
    user.save()
    return user

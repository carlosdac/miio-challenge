from django.contrib.auth.models import User
from rest_framework import serializers

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
      'id': {
          'read_only': True
      }
    }

  def create(self):
    user = User(
      username=self.validated_data['username'],
      email=self.validated_data['email'],
      first_name=self.validated_data['first_name'],
      last_name=self.validated_data['last_name']
    )
    user.set_password(self.validated_data['password'])
    user.save()
    return user

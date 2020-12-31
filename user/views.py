from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .utils import is_authenticated
from .serializers import UserSerializer
from .exceptions import NonAuthorized
# Create your views here.


"""
This View makes a user registration. It implements the create method from ModelViewSet how to POST
and recieves all fields of User Django in request body.
"""
class UserView(ModelViewSet):
	parser_classes = (JSONParser,)
	serializer_class = UserSerializer
	permission_classes = [AllowAny]

	def create(self, request, *args, **kwargs):
		return super(UserView, self).create(request, *args, **kwargs)
from django.shortcuts import render
from user.utils import is_authenticated

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import RegularPlan
from user.utils import is_authenticated
from .serializers import RegularPlanSerializer
from user.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from miio_challenge.celery import send_mail, save_mongodb
# Create your views here.


class RegularPlanView(ModelViewSet):

	parser_classes = (JSONParser,)
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = RegularPlanSerializer


	def get_queryset(self):
		user = is_authenticated(self.request)
		publish = self.request.query_params.get("publish", None)
		
		if publish != None:
			queryset = RegularPlan.objects.filter(publish=True)
		else:
			queryset = RegularPlan.objects.filter(owner=user)
		return queryset



	def create(self, request, *args, **kwargs):
		user = is_authenticated(request)

		request.data['owner_id'] = user.id
		response = super(RegularPlanView, self).create(request, *args, **kwargs)

		save_mongodb.delay(response.data, 'regularPlans')
		
		return response

	def partial_update(self, request, *args, **kwargs):
		user = is_authenticated(request)
		request.data['owner_id'] = user.id
		return super(RegularPlanView, self).partial_update(request, *args, **kwargs)
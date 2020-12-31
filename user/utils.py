from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .exceptions import NonAuthorized

"""
This method verify if a user is authenticated in request. A user is authenticated if request.user is a instance
of User Django Model, else this user is a instance of AnonymousUser.
"""
def is_authenticated(request):
	if isinstance(request.user, User):
		return request.user
	raise NonAuthorized()

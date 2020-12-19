from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .exceptions import NonAuthorized


def is_authenticated(request):
	if not isinstance(request.user, User):
		raise NonAuthorized()
	return request.user

def generate_token_to_user(user):
	jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
	jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
	payload = jwt_payload_handler(user)
	token = jwt_encode_handler(payload)
	return token
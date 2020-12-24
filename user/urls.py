from django.urls import path
from .views import UserView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
  
  path('register/', UserView.as_view({'post': 'create'}), name="register"),
  path('login/', obtain_jwt_token, name="login"),
]

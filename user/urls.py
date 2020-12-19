from django.urls import path
from .views import UserRegisterView, UserLoginView
urlpatterns = [
  
  path('register/', UserRegisterView.as_view({'post': 'create'})),
  path('login/', UserLoginView.as_view({'post': 'create'})),
]

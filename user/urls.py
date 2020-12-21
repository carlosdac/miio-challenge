from django.urls import path
from .views import UserView
urlpatterns = [
  
  path('register/', UserView.as_view({'post': 'create'}), name="register"),
  path('login/', UserView.as_view({'post': 'login'}), name="login"),
]

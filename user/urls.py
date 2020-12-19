from django.urls import path

urlpatterns = [
  
  path('register/', UserRegisterView.as_view({'post': 'create'})),
]

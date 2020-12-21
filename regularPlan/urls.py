from django.urls import path
from .views import RegularPlanView

urlpatterns = [
  path('', RegularPlanView.as_view({'post': 'create', 'get': 'list',})),
  path('<int:pk>/', RegularPlanView.as_view({'patch': 'partial_update', 'get': 'retrieve',}))
]

from django.urls import path
from .views import RegularPlanView

urlpatterns = [
  path('', RegularPlanView.as_view({'post': 'create', 'get': 'list',}), name="create or list"),
  path('<int:pk>/', RegularPlanView.as_view({'patch': 'partial_update',}), name="update")
]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.law_select, name='law_select'),
    path('parameters/<law_name>/', views.param_select, name='param_select')
]

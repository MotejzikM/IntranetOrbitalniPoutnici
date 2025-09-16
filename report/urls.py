from django.urls import path, include
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.index, name='index'),  # Main page of the report app
]
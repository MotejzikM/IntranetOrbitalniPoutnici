from django.urls import path, include
from . import views

app_name = 'diskuze'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:id>/', views.diskuze_detail, name='diskuze_detail'),
    path('add_message/<int:id>/', views.add_message, name='add_message'),
    path('add_discussion/', views.add_discussion, name='add_discussion'),
    path('delete_discussion/<int:id>/', views.delete_discussion, name='delete_discussion'),
]
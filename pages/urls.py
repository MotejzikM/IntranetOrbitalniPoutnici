from . import views
from django.urls import path, include

app_name = 'pages'

urlpatterns = [
    path('', views.page_list, name='page_list'),
    path('add/', views.add_page, name='add_page'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),
    path('<slug:slug>/edit/', views.edit_page, name='edit_page'),
    # Add more URLs for the pages app as needed
]
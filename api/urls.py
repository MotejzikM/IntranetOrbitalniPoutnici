from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pages.views import PageViewSet
from diskuze.views import DiskuzeViewSet
from kalendar.views import EventViewSet

router = DefaultRouter()
router.register(r'pages', PageViewSet)
router.register(r'diskuze', DiskuzeViewSet)

# Přidej další routery zde...

urlpatterns = [
    path('', include(router.urls)),
    path('kalendar/', include('kalendar.urls')),
    path('diskuze/', include('diskuze.urls')),
    path('pages/', include('pages.urls')),
    path('api-auth/', include('rest_framework.urls')),  # Prohlížeč API


]
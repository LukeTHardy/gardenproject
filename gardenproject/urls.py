from django.contrib import admin
from django.urls import include, path
from gardenapi.views import register_user, login_user
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from gardenapi.views import ZoneViewSet, WaterViewSet, LightViewSet, SoilViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'zones', ZoneViewSet, 'zone')
router.register(r'lights', LightViewSet, 'light')
router.register(r'soils', SoilViewSet, 'soil')
router.register(r'waters', WaterViewSet, 'water')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


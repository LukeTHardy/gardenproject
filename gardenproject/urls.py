from django.contrib import admin
from django.urls import include, path
from gardenapi.views import register_user, login_user
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from gardenapi.views import ZoneViewSet, WaterViewSet, LightViewSet, SoilViewSet, CritterTypeViewSet, VeggieCatViewSet, PlantTypeViewSet, FavoriteViewSet, PlantCritterPairingViewSet, PlantZonePairingViewSet, CompanionPairingViewSet, PlantViewSet, CritterViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'zones', ZoneViewSet, 'zone')
router.register(r'lights', LightViewSet, 'light')
router.register(r'soils', SoilViewSet, 'soil')
router.register(r'waters', WaterViewSet, 'water')
router.register(r'crittertypes', CritterTypeViewSet, 'crittertype')
router.register(r'veggiecats', VeggieCatViewSet, 'veggiecat')
router.register(r'planttypes', PlantTypeViewSet, 'planttype')
router.register(r'favorites', FavoriteViewSet, 'favorite')
router.register(r'plantcritterpairings', PlantCritterPairingViewSet, 'plantcritterpairing')
router.register(r'plantzonepairings', PlantZonePairingViewSet, 'plantzonepairing')
router.register(r'companionpairings', CompanionPairingViewSet, 'companionpairing')
router.register(r'plants', PlantViewSet, 'plant')
router.register(r'critters', CritterViewSet, 'critter')




urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
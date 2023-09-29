from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()

#registrando rutas
#al hacer la peticion desde el front siempre poner una  / al final de la ruta ejemplo -> api/colors/
router.register(r'api/colors', viewsets.ColorViewSet, basename='colors')
router.register(r'api/products', viewsets.ProductViewSet, basename='colors')

urlpatterns = router.urls


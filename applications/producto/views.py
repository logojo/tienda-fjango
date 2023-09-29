from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import render

from .models import Product
from .serializers import ProductSerializer

# Lista los productos creados por usuario
class ProductView(ListAPIView):
    serializer_class = ProductSerializer
    #identificando y autentiando al usuario logueado por token
    authentication_classes = (TokenAuthentication,)
    #solicitando que solo se pueda entrar a esta vista un usuario logueado (permisos de la vista)
    #ReadOnly permisos de solo lectura a la vista
    permission_classes = [IsAuthenticated]
    #permiso de ingreso a la vista solo para usuario administrador
    ##permission_classes = [IsAdminUser]
    def get_queryset(self): 
        #recuperando usuario
        user = self.request.user   
        return Product.objects.productsByUser(user)
    

class ProductStockView(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    #permission_classes = [IsAuthenticated, IsAdminUser]
    def get_queryset(self): 
        #recuperando usuario
        user = self.request.user   
        return Product.objects.productsWithStock()
    
class ProductGeneroView(ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self): 
        #recuperando parametro por url
        genero = self.kwargs['gender']
        return Product.objects.productsByGender(genero)
    
class ProductFiltersView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self): 
        m = self.request.query_params.get('woman', None)
        h = self.request.query_params.get('man', None)
        nombre = self.request.query_params.get('name', None)
        print(m)
        print(h)
        print(nombre)
        return Product.objects.productsByFilter(
            woman = m, 
            man = h, 
            name = nombre
        )
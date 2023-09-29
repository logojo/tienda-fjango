from django.shortcuts import render
from django.utils import timezone

from rest_framework.generics import ( ListAPIView, CreateAPIView )
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Sale, SaleDetail, Product
from .serializers import SaleSerializers, ProcesoVentaSerializer, ProcesoVentaSerializer2

# Create your views here.
class SalesReport( ListAPIView ):
    serializer_class = SaleSerializers

    def get_queryset(self):       
        return Sale.objects.all()


#Vista para crear ventas
class SaleView( CreateAPIView ):
    """ vista  de registro de venta de un producto"""
    serializer_class = ProcesoVentaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    

    # Sobreescribiendo la función create para recuperar los datos y poder almacenarlos en la tabla 
    # Ya que el serializador no esta vinculado a un modelo
    def create(self, request, *args, **kwargs):
        #esta variable puede ir con cualquier nombre
        #serializando los datos que vienen del request
        serializer = ProcesoVentaSerializer(data=request.data)

        #validando que los datos vengan como lo pide el serializador, si no, manda un error      
        serializer.is_valid(raise_exception=True)

         #esto se puede hacer tambien con un if
         #   if data.is_valid():
                # acciones 
         #   else:
               # error
        
        venta = Sale.objects.create(
            date_sale = timezone.now(),
            amount = 0,
            count = 0,
            type_invoce = serializer.validated_data['type_invoce'],
            type_payment = serializer.validated_data['type_payment'],
            adreese_send = serializer.validated_data['adreese_send'],
            user = self.request.user,
        )

        #recuperando productos de la venta enviados en el request
        productos = serializer.validated_data['productos']
        ventas_detail = []
        totalSale = 0
        totalProducts = 0

        for producto in productos:  
            #recuperando un producto desde la base de datos
            prod = Product.objects.get(id=producto['pk'])
            venta_detail = SaleDetail(
                sale = venta,
                product = prod,
                count = producto['amount'],
                price_purchase = prod.price_purchase,
                price_sale = prod.price_sale,
            )

            totalSale = totalSale + prod.price_sale * producto['amount']
            totalProducts = totalProducts + producto['amount']

            #agregando elementos al array
            ventas_detail.append( venta_detail )


        # actualizando datos de la venta 
        venta.amount = totalSale
        venta.count = totalProducts
        venta.save()

        #almacenado array de productos en bd
        SaleDetail.objects.bulk_create( ventas_detail )
 
        return Response({'success': True})
    
class SaleCustomView( CreateAPIView ):
    """ vista  de registro de venta de un producto mejorada de la anterior"""

    serializer_class = ProcesoVentaSerializer2
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ProcesoVentaSerializer2(data=request.data) 
        serializer.is_valid(raise_exception=True)
        
        venta = Sale.objects.create(
            date_sale = timezone.now(),
            amount = 0,
            count = 0,
            type_invoce = serializer.validated_data['type_invoce'],
            type_payment = serializer.validated_data['type_payment'],
            adreese_send = serializer.validated_data['adreese_send'],
            user = self.request.user,
        )

        #recuperando los ids de los productos enviados en el request desde la base de datos
        productos = Product.objects.filter(id__in=serializer.validated_data['productos'])
        cantidades = serializer.validated_data['amounts']
        ventas_detail = []
        totalSale = 0
        totalProducts = 0

        #en este for se estan iterando dos arreglos al mismo tiempo
        for producto, cantidad in zip(productos, cantidades):
            venta_detail = SaleDetail(
                sale = venta,
                product = producto,
                count = cantidad,
                price_purchase = producto.price_purchase,
                price_sale = producto.price_sale,
            )

            totalSale = totalSale + producto.price_sale * cantidad
            totalProducts = totalProducts + cantidad

            #agregando elementos al array
            ventas_detail.append( venta_detail )


        # actualizando datos de la venta 
        venta.amount = totalSale
        venta.count = totalProducts
        venta.save()

        #almacenado array de productos en bd
        SaleDetail.objects.bulk_create( ventas_detail )
 
        return Response({'success': True})
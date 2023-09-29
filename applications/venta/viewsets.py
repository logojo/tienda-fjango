from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Sale, SaleDetail, Product
from .serializers import SaleSerializers, ProcesoVentaSerializer2


class VentasViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)

    #al sobreescribir esta funcion podemos indicar permisos independientes para cada función
    def get_permissions(self):
        if ( self.action == 'list' ) or ( self.action == 'retrieve' ):
             permission_classes = [AllowAny]
        else: 
             permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    


    # Cuando se utiliza un viewset que no esta ligado a un modelo es decir no se utiliza el metodo "ModelViewSet"
    # Es necesario definir todos sus metodos para que el viewset identifique que hacer y sobre que modelos trabajar en cada uno de ellos
    def list(self, request):
        queryset = Sale.objects.all()
        serializer = SaleSerializers(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
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
 
        sale = Sale.objects.get(id=venta.id)
        serializer = SaleSerializers(sale)
        return Response(serializer.data)

    #esta es un show como en laravel
    def retrieve(self, request, pk=None):
        #sale = Sale.objects.get(id=pk)
        #manejo de excepciones en caso de que no encuentre el registro
        sale =  get_object_or_404( Sale.objects.all(), pk=pk) 
        serializer = SaleSerializers(sale)
        return Response(serializer.data)

    def update(self, request, pk=None):
        return Response({"success": True})

    #y este es un metodo PATH
    def partial_update(self, request, pk=None):
        return Response({"success": True})

    def destroy(self, request, pk=None):
        return Response({"success": True})
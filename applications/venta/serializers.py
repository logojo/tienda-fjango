from rest_framework import serializers
from .models import Sale, SaleDetail

class SaleSerializers(serializers.ModelSerializer):
    productos  = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = (
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'adreese_send',
            'user',
            'productos'
        )
    
    #object representa a cada uno de los registros que hay la tabla Sale
    def get_productos(self, object):
       query = SaleDetail.objects.saleDetails(object.id)
       productos_serializados =  SaleDetailSerializers(query, many=True).data
       return productos_serializados


class SaleDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = (
            'id',
            'sale',
            'product',
            'count',
            'price_purchase',
            'price_sale',
            'anulate',
        )


class ProductDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    amount = serializers.IntegerField()


class ProcesoVentaSerializer(serializers.Serializer):
    type_invoce = serializers.CharField()
    type_payment  = serializers.CharField()
    adreese_send  = serializers.CharField()
    #este campo es del tipo de un serializer definido
    productos  = ProductDetailSerializer(many=True,)


#ListFieldSerializer
#serializador de tipo array
class ArrayIntegerSerializer(serializers.ListField):
   child = serializers.IntegerField()

class ProcesoVentaSerializer2(serializers.Serializer):
    type_invoce = serializers.CharField()
    type_payment  = serializers.CharField()
    adreese_send  = serializers.CharField()
    #este campo es del tipo de un serializer definido
    productos  = ArrayIntegerSerializer()
    amounts  = ArrayIntegerSerializer()


    #validaciones en el serializador generales(todos los campos)
    def validate(self, data):
        if data['type_payment'] != '0':
            raise serializers.ValidationError('Ingrese un tipo de pago correcto')

    #validaciones en el serializador personalizada(campo en particular)
    def validate_type_invoce(self, value):
        if value != '0':
            raise serializers.ValidationError('Ingrese un valor correcto')
        
        return value

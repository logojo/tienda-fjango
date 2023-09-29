from rest_framework import serializers, pagination

from .models import Product, Colors

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ( 'color', )

class ProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many = True)
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'man',
            'woman',
            'weight',
            'price_purchase',
            'price_sale',
            'main_image',
            'image1',
            'image2',
            'image3',
            'image4',
            'colors',
            'video',
            'stok',
            'num_sales',
            'user_created'
        )

class ProductSerializerViewSet(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ( '__all__')

class PaginationSerializer(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 50
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Colors, Product
from .serializers import ColorSerializer,ProductSerializer, ProductSerializerViewSet, PaginationSerializer

#los viewsets te controlan todas las funciones de un crud de una manera muy resumida
#los viewsets se pueden trabajar igualmente en el archivo views
class ColorViewSet(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Colors.objects.all()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializerViewSet
    queryset = Product.objects.all()
    pagination_class = PaginationSerializer

    #de esta manera sobreescribo el metodo get para mostrar los datos utilizando un serializador diferente al que se utiliza para guardar los datos
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
    #esta función se utiliza para ealizar cambios en los datos antes de ser guardados
    def perform_create(self, serializer):
        serializer.save(
            video = 'https://www.youtube.com/results?search_query=crud+django+mysql'
        )
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import ProductType, Product


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttype',
            lookup_field= 'id'
        )
        fields = ('id', 'name', 'products')

        depth = 1
        
class ProductTypes(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            ptype = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(
                ptype, context={'request': request}
            )
            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        
        ptypes = ProductType.objects.all()
        
        serializer = ProductTypeSerializer(
            ptypes, many=True, context={'request': request})
        
        return Response(serializer.data)
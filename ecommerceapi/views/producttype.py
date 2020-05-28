from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import ProductType


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttype',
            lookup_field= 'id'
        )
        fields = ('id', 'name')
        
class ProductTypes(ViewSet):
    
    def list(self, request):
        
        producttypes = ProductType.objects.all()
        
        categories=dict()
        
        for producttype in producttypes:
            categories.update(producttype)
            print(producttype, "PRODUCT TYPES!!!!!!!!")

        serializer = ProductTypeSerializer(
            producttypes, many=True, context={'request': request})
        
        return Response(serializer.data)
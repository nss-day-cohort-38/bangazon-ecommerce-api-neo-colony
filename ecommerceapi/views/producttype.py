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
        fields = ('id', 'name')
        
class ProductTypes(ViewSet):
    
    def list(self, request):
        
        ptypes = ProductType.objects.all()
      
        for ptype in ptypes:
            ptype.total = len(Product.objects.filter(product_type_id=ptype.id))
            ptype.products = Product.objects.filter(product_type_id=ptype.id).order_by('-id')[:3]

        serializer = ProductTypeSerializer(
            ptypes, many=True, context={'request': request})
        
        return Response(serializer.data)
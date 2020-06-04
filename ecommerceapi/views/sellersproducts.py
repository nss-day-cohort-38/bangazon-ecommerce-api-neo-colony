from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'title', 'customer_id', 'price', 'description',
                  'quantity', 'location', 'image_path', 'created_at', 'product_type_id')


class MyProducts(ViewSet):

    def list(self, request):

        sellers_products = Product.objects.filter(customer_id=request.auth.user.id)

        serializer = ProductSerializer(
            sellers_products, many=True, context={'request': request}
        )

        return Response(serializer.data)
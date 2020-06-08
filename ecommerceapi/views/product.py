from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'title', 'customer_id', 'price', 'description',
                  'quantity', 'location', 'image', 'created_at', 'product_type_id')


class Products(ViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def create(self, request):
    
        new_product = Product()
        new_product.title = request.data["title"]
        new_product.price = request.data["price"]
        new_product.description = request.data["description"]
        new_product.quantity = request.data["quantity"]
        new_product.location = request.data["location"]
        new_product.image = request.data["image"]
        new_product.product_type_id = request.data["product_type_id"]

        customer = Customer.objects.get(user_id=request.auth.user.id)
        new_product.customer = customer
        new_product.save()

        serializer = ProductSerializer(
            new_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(
                product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual product

        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)
        product.title = request.data["title"]
        product.price = request.data["price"]
        product.description = request.data["description"]
        product.quantity = request.data["quantity"]
        product.location = request.data["location"]
        product.image = request.data["image"]
        product.product_type_id = request.data["product_type_id"]
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        products = Product.objects.all()

        total = self.request.query_params.get('total')

        search_term = self.request.query_params.get('title')

        location = self.request.query_params.get('location')

        category_id = self.request.query_params.get('category')

        seller = self.request.query_params.get('seller')

        if total is not None:
            products = Product.objects.order_by('-id')[:int(total)]

        if search_term is not None:
            products = Product.objects.filter(title__icontains=search_term)
        
        if location is not None:
            products = Product.objects.filter(location__icontains = location)

        if category_id is not None:
            products = Product.objects.filter(product_type_id=category_id)

        if seller is not None:
            customer = Customer.objects.get(user_id = request.auth.user.id)
            products = Product.objects.filter(customer_id = customer.id)

        serializer = ProductSerializer(
            products, many=True, context={'request': request})

        return Response(serializer.data)

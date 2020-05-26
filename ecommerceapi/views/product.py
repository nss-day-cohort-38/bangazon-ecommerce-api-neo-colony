from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'title', 'customer_id', 'price', 'description', 
                  'quantity', 'location', 'image_path', 'created_at', 'product_type_id')

class Products(ViewSet):

    def create(self, request):
            """Handle POST operations

            Returns:
                Response -- JSON serialized Attraction instance
            """
            new_product = Product()
            new_product.title = request.data["title"]
            new_product.price = request.data["price"]
            new_product.description = request.data["description"]
            new_product.quantity = request.data["quantity"]
            new_product.location = request.data["location"]
            new_product.image_path = request.data["image_path"]
            new_product.product_type_id = request.data["product_type_id"]

            customer = Customer.objects.get(pk=request.data["customer_id"])
            new_product.customer = customer
            new_product.save()

            serializer = ProductSerializer(new_product, context={'request': request})

            return Response(serializer.data)
        
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
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
        product.image_path = request.data["image_path"]
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
        product = Product.objects.all()
        serializer = ProductSerializer(
            product, many=True, context={'request': request})
        return Response(serializer.data)
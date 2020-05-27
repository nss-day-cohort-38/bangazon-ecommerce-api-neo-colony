from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer,Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'customer_id', 'payment_type_id', 'created_at')


class Orders(ViewSet):

    def create(self, request):
   
        new_order = Order()
        new_order.payment_type_id = request.data["payment_type_id"]
       

        customer = Customer.objects.get(pk=request.data["customer_id"])
        new_product.customer = customer
        new_product.save()

        serializer = ProductSerializer(
            new_product, context={'request': request})

        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     try:
    #         product = Product.objects.get(pk=pk)
    #         serializer = ProductSerializer(
    #             product, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def put(self, request, pk=None):
    #     """Handle PUT requests for an individual product

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     product = Product.objects.get(pk=pk)
    #     product.title = request.data["title"]
    #     product.price = request.data["price"]
    #     product.description = request.data["description"]
    #     product.quantity = request.data["quantity"]
    #     product.location = request.data["location"]
    #     product.image_path = request.data["image_path"]
    #     product.product_type_id = request.data["product_type_id"]
    #     product.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single product

    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         product = Product.objects.get(pk=pk)
    #         product.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except Product.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request):
        
    #     products = Product.objects.all()

    #     total = self.request.query_params.get('total')

    #     search_term = self.request.query_params.get('title')

    #     location = self.request.query_params.get('location')

    #     if total is not None:
    #         products = Product.objects.order_by('-id')[:int(total)]

    #     if search_term is not None:
    #         products = Product.objects.filter(title__icontains=search_term)
        
    #     if location is not None:
    #         products = Product.objects.filter(location__icontains = location)

    #     serializer = ProductSerializer(
    #         products, many=True, context={'request': request})

    #     return Response(serializer.data)

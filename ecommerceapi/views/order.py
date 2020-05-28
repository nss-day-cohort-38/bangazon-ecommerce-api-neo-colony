from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer,Order, PaymentType


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
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_order = Order()
        payment_type = PaymentType.objects.get(pk=request.data["payment_type_id"])
        new_order.payment_type = payment_type
        customer = Customer.objects.get(pk=request.data["customer_id"])
        new_order.customer = customer
        new_order.save()

        serializer = OrderSerializer(
            new_order, context={'request': request})

        return Response(serializer.data)

def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(
                order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

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

def list(self, request):
        
        order = Order.objects.all()

        serializer = OrderSerializer(
            order, many=True, context={'request': request})

        return Response(serializer.data)

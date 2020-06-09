from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer, Order, PaymentType


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'customer_id', 'payment_type_id', 'orderproducts', 'created_at')
        depth = 2


class Orders(ViewSet):

    def create(self, request):

        customer = Customer.objects.get(user=request.auth.user)
        new_order = Order()
        new_order.customer = customer
        new_order.payment_type_id = None

        new_order.save()

        serialize = OrderSerializer(new_order, context={'request': request}) 
        return Response(serialize.data)


    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(
                order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request, pk=None):
        
        order = Order.objects.filter(customer_id = request.auth.user.id, payment_type_id__isnull=False)
        serializer = OrderSerializer(order, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):

        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def update(self, request, pk=None):
        customer = Customer.objects.get(user_id=request.auth.user.id)
        order = Order.objects.get(customer_id= customer.id, payment_type=None)
        order.payment_type_id = request.data['payment_type_id']
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

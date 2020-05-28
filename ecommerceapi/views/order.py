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
        
        order = Order.objects.filter(customer_id = request.auth.user.id)
        serializer = OrderSerializer(order, many=True, context={'request': request})

        return Response(serializer.data)

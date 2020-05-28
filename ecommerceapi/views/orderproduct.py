from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer, Order, PaymentType, OrderProduct


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderProducts
        url = serializers.HyperlinkedIdentityField(
            view_name='order_product',
            lookup_field='id'
        )
        fields = ('id', 'order_id', 'product_id')

class OrderProducts(ViewSet):   

    def create(self, request):

        customer = Customer.objects.filter(user_id = request.auth.user.id)
        order = Order.object.filter(customer_id=customer.id, payment_type=None)

        if order is None:

            new_order = Order()
            new_order.customer_id = customer.id
            new_order.save()

            new_order_product = OrderProduct()
            new_order_product.customer_id = customer.id
            new_order_product.order_id = new_order.id

            new_order_product.save()

            # serialize = OrderProductSerializer(new_order_product, context={'request': request}) 
        
        else:

            new_order_product = OrderProduct()
            new_order_product.customer_id = customer.id
            new_order_product.order_id = order.id

            new_order_product.save()

        serialize = OrderProductSerializer(new_order_product, context={'request': request}) 
        return Response(serialize.data) 
                

    def retrieve(self, request, pk=None):
        try:
            order_product = OrderProducts.objects.get(pk=pk)
            serializer = OrderProductSerializer(
                order_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

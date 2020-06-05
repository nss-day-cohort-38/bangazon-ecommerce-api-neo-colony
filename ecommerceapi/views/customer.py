from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer
from django.contrib.auth.models import User
from .user import Users


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Customers

    Arguments:
        serializers
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'address', 'phone_number', 'user')
        depth = 1

class Customers(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        customer = Customer.objects.get(pk=pk)
        customer.address = request.data['address']
        customer.phone_number = request.data['phone_number']
        

        customer.save()

        user = User.objects.get(pk=customer.user_id)
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.email = request.data['email']
        
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):

        customer = Customer.objects.filter(user_id=request.auth.user.id)

        serializer = CustomerSerializer(
            customer, many=True, context={'request': request})

        return Response(serializer.data)    



        
    

            
            
            

        
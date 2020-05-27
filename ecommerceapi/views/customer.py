from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer
from django.contrib.auth.models import User


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

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
    
    # def create(self, request):

    #     newuser = User()
    #     newuser.first_name = request.data['first_name']
    #     newuser.last_name = request.data['last_name']
    #     newuser.password = request.data['password']
    #     newuser.email = request.data['email']
        
    #     newuser.save()

    #     newcustomer = Customer()
    #     newcustomer.address = request.data['address']
    #     newcustomer.phone_number = request.data['phone_number']
    #     newcustomer.user_id = newuser.id

    #     newcustomer.save()

    #     serializer = CustomerSerializer(newcustomer, context={'request': request})

    #     return Response(serializer.data)

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

    def destroy(self, request, pk=None):

        try:
            customer = Customer.objects.get(pk=pk)
            customer.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Customer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
    

            
            
            

        
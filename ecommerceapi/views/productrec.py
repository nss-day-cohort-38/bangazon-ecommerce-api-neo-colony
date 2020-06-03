from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import ProductRec, Customer


class ProductRecSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductRec
        url = serializers.HyperlinkedIdentityField(
            view_name='productrec',
            lookup_field='id'
        )
        fields = ('id', 'sender_id', 'reciever_id')

class ProductRecs(ViewSet):

    def create(self, request):

        user_customer_object = Customer.objects.get(user_id=request.auth.user.id)

        new_productrec = ProductRec()
        new_productrec.sender_id =  user_customer_object.id
        new_productrec.reciever_id = request.data['reciever_id']
        new_productrec.product_id = request.data['product_id']

        new_productrec.save()

        serializer = ProductRecSerializer(
            new_productrec, context={'request': request})
        
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            productrec = ProductRec.objects.get(pk=pk)
            serializer = ProductRecSerializer(
                productrec, context={'request': request}
            )
            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        
        try:
            customer = Customer.objects.get(user_id=request.auth.user.id)
            print('xxxxxxxxx', customer.id, 'xxxxxxx')
            
            productrecs = ProductRec.objects.filter(reciever_id=customer.id)
        
            serializer = ProductRecSerializer(
                productrecs, many=True, context={'request': request})
            
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
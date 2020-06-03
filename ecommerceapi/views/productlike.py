from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import ProductLike, Customer, Product

class ProductLikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductLike
        url = serializers.HyperlinkedIdentityField(
            view_name='productlike',
            lookup_field='id'
        )
        fields = ('id', 'like', 'customer_id', 'product_id')
        
class ProductLikes(ViewSet):
    
    def create(self, request):
        
        customer = Customer.objects.get(user=request.auth.user)
        new_productlike = ProductLike()
        new_productlike.like = request.data["like"]
        new_productlike.customer_id = customer.id
        new_productlike.product_id = request.data["product_id"]
        
        new_productlike.save()
        
        serialize = ProductLikeSerializer(new_productlike, context={'request': request})
        
        return Response(serialize.data)
    
    def retrieve(self, request, pk=None):
        try:
            productlike = ProductLike.objects.get(pk=pk)
            serializer = ProductLikeSerializer(
                productlike, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def destroy(self, request, pk=None):
    
        try:
            productlike = ProductLike.objects.get(pk=pk)
            productlike.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductLike.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):
        
        productlike = ProductLike.objects.get(pk=pk)
        productlike.like =request.data['like']
        
        productlike.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
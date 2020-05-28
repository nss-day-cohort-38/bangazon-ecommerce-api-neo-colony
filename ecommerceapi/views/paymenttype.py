from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import PaymentType, Customer


class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'merchant_name', 'account_number', 'expiration_date', 'created_at',
                  'customer_id')


class PaymentTypes(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_payment_type = PaymentType()
        new_payment_type.merchant_name = request.data["merchant_name"]
        new_payment_type.account_number = request.data["account_number"]
        new_payment_type.expiration_date = request.data["expiration_date"]

        customer = Customer.objects.get(pk=request.data["customer_id"])
        new_payment_type.customer = customer
        new_payment_type.save()

        serializer = PaymentTypeSerializer(
            new_payment_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            paymenttype = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(
                paymenttype, context={'request': request})
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

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single payment type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            payment_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        payment_type = PaymentType.objects.all()

        serializer = PaymentTypeSerializer(
            payment_type, many=True, context={'request': request})

        return Response(serializer.data)

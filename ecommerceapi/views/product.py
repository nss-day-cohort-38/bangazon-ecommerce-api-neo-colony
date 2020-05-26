# Given the user is not authenticated
# When any view renders
# Then the Sell a Product affordance will not be visible

# Given the user is authenticated
# When the user clicks on the Sell a product button in the menu bar
# Then the user will be presented with a product form

# Given the user has filled in all fields of the product form with any invalid information
# When the user clicks the Sell button
# Then the user will be immediately notified with error information for each invalid value
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='attraction',
            lookup_field='id'
        )
        fields = ('id', 'title', 'customer_id', 'price', 'description', 
                  'quantity', 'location', 'image_path', 'created_at', 'product_type_id')

class Products(ViewSet):

    def create(self, request):
            """Handle POST operations

            Returns:
                Response -- JSON serialized Attraction instance
            """
            new_product = Product()
            new_product.title = request.data["title"]
            new_product.price = request.data["price"]
            new_product.description = request.data["description"]
            new_product.quantity = request.data["quantity"]
            new_product.location = request.data["location"]
            new_product.image_path = request.data["image_path"]

            customer = Customer.objects.get(pk=request.data["customer_id"])
            new_product.customer = customer
            new_product.save()

            serializer = ProductSerializer(new_product, context={'request': request})

            return Response(serializer.data)
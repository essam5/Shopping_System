from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import AddressSerializer, UserMiniSerializer
from product.serializers import ProductDetailSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ["updated"]


class OrderMiniSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    buyer = UserMiniSerializer(required=False)

    class Meta:
        model = Order
        exclude = ["updated"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ["updated"]


class OrderItemMiniSerializer(serializers.ModelSerializer):
    order = OrderMiniSerializer(required=False, read_only=True)
    product = ProductDetailSerializer(required=False, read_only=True)

    class Meta:
        model = OrderItem
        exclude = ["updated"]

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, exceptions
from .serializers import (
    OrderItemMiniSerializer,
    OrderSerializer,
)
from rest_framework import viewsets, permissions
from .models import Order, OrderItem
from users.models import Address
from .models import Product
from core_app.decorators import time_calculator
from product.permissions import IsOwnerAuth


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @time_calculator
    def time(self):
        return 0

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        user_address = Address.objects.filter(user=user, primary=True).first()
        product = get_object_or_404(Product, pk=pk)
        if product.quantity == 0:
            raise exceptions.NotAcceptable("quantity of this product is out.")
        try:
            order_number = request.data.get("order_number", "")
            quantity = request.data.get("quantity", 1)
        except:
            pass

        total = quantity * product.price
        order = Order().create_order(user, order_number, user_address, True)
        order_item = OrderItem().create_order_item(order, product, quantity, total)
        serializer = OrderItemMiniSerializer(order_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-id")
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerAuth)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(buyer=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

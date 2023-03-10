from contextlib import suppress
from datetime import timedelta, datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.ecommerce.filters import ProductFilter
from apps.ecommerce.models import Category, Shop, Product, Cart, Wishlist, Order
from apps.ecommerce.serializers import CategoryModelSerializer, ShopModelSerializer, ProductModelSerializer, \
    WishlistModelSerializer, OrderCreateModelSerializer, CartModelSerializer
from apps.user.permissions import IsOwner


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

class ShopModelViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopModelSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['price']
    permission_classes = (IsAuthenticated, IsOwner,)

    def perform_create(self, serializer):
        # when a product is saved, its saved how it is the owner
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # after get all products on DB it will be filtered by its owner and return the queryset
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    @action(['GET'], False, 'report', 'report')
    def get_carts_count(self, request):
        count = self.get_queryset().filter(status='accepted').aggregate(Sum('quantity'))
        return Response({'Sotilgan mahsulot: ': count.get('quantity__sum')})
    # @action(['GET'], False, 'report', 'report')
    # def get_carts_count(self, request):
    #     last_month = datetime.today() - timedelta(days=30)
    #     qs = self.get_queryset()
    #     count = qs.filter(created_at__gte=last_month, status='accepted').aggregate(Sum('quantity'))
    #     shop = Shop.name
    #     return Response(
    #         {
    #             'shop': shop,
    #             'test': count.get('quantity__sum')
    #         }
    #     )


class WishlistModelViewSet(ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistModelSerializer


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateModelSerializer
    permission_classes = (IsAuthenticated, IsOwner,)

    def get_queryset(self):
        qs = super().get_queryset()
        data = self.request.data
        cart, product = data.get('cart'), data.get('product')
        with suppress(Exception):
            quantity = Cart.objects.get(pk=cart).quantity
            Product.objects.filter(pk=product).update(amount=F('amount') - quantity)
            Cart.objects.filter(pk=cart).update(status='accepted')
            return qs

from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.ecommerce.models import Category, Shop, Product, Cart, Wishlist, Order


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ShopModelSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartModelSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class WishlistModelSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class OrderCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'product', 'cart', 'user')
        # fields = '__all__'


class CartReportModelSerializer(ModelSerializer):
    count = SerializerMethodField()


    class Meta:
        model = Cart
        fields = ()

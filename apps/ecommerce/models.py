from django.contrib.auth.models import User
from django.db.models import Model, CharField, ImageField, ForeignKey, CASCADE, IntegerField, \
    DateTimeField, SET_NULL, DecimalField, TextChoices, PositiveIntegerField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(MPTTModel):
    name = CharField(max_length=255)
    parent = TreeForeignKey('self', SET_NULL, related_name='category', null=True, blank=True)

    def __str__(self):
        return self.name


class Shop(BaseModel):
    name = CharField(max_length=50)
    description = CharField(max_length=512)
    image = ImageField(upload_to='shop_image/', null=True, blank=True)
    merchant = ForeignKey('user.User', CASCADE, related_name='merchant', null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = CharField(max_length=255)
    description = CharField(max_length=1000)
    image = ImageField(upload_to='images/', null=True, blank=True)
    price = DecimalField(max_digits=9, decimal_places=2)
    amount = IntegerField(default=1)
    category = ForeignKey(Category, CASCADE, related_name='product', null=True, blank=True)
    shop = ForeignKey(Shop, CASCADE, related_name='shop', null=True, blank=True)
    owner = ForeignKey('user.User', CASCADE, related_name='owner', null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(BaseModel):
    class CartStatus(TextChoices):
        ACCEPTED = 'accepted', 'Accepted'
        PENDING = 'pending', 'Pending'

    product = ForeignKey('ecommerce.Product', CASCADE)
    user = ForeignKey('user.User', CASCADE)
    quantity = PositiveIntegerField(default=1)
    status = CharField(max_length=20, choices=CartStatus.choices, default=CartStatus.PENDING)

    def __str__(self):
        return f'{self.product}'


class Order(BaseModel):
    user = ForeignKey('user.User', CASCADE)
    cart = ForeignKey('ecommerce.Cart', CASCADE)
    product = ForeignKey('ecommerce.Product', CASCADE)

    def __str__(self):
        return f"{self.product.name}"


class Wishlist(BaseModel):
    product = ForeignKey('ecommerce.Product', CASCADE)
    user = ForeignKey('user.User', CASCADE)

    def __str__(self):
        return f'{self.product}'

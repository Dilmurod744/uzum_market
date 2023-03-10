from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from apps.ecommerce.models import Category, Shop, Product, Cart, Wishlist, Order


@admin.register(Category)
class CategoryMPTTModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20


admin.site.register(Shop)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'image_show', 'price']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ProductAdmin, self).get_queryset(request)

        #     return super(ProductAdmin, self).get_queryset(request)
        else:
            qs = super(ProductAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='150' />".format(obj.image.url))

        return 'None'

    image_show.__name__ = 'images'

# admin.site.register(Product, ProductAdmin)

from inventory.models import Brand, Category, Product, ProductImage
from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    pass


class ProductImageAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class BrandAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
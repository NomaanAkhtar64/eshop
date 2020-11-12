from inventory.models import Brand, Category, Color, Dimension, Product, ProductImage
from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Naming", {"fields": ["name", "slug"]}),
        ("Photographs", {"fields": ["main_image", "thumbnail_image"]}),
        ("Controls", {"fields": ["is_active", "on_sale"]}),
        ("Categorization", {"fields": ["category", "brand"]}),
        (
            "Economics",
            {"fields": ["base_price", "sale_price", "sale_percentage"]},
        ),
        ("Stats", {"fields": ["sold"]}),
        ("Physical Features", {"fields": ["dimensions", "colors"]}),
        ("Feedback", {"fields": ["reviews"]}),
    )
    list_display = ("name", "sale_price")
    readonly_fields = (
        "slug",
        "reviews",
        "sold",
    )


class ProductImageAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    readonly_fields = ("slug",)


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "logo",
    )
    readonly_fields = ("slug",)


class DimensionAdmin(admin.ModelAdmin):
    class Media:
        js = ("inventory/admin/dimension.js",)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Dimension, DimensionAdmin)
admin.site.register(Color)
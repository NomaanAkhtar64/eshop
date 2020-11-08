from inventory.utils import get_ext
from django.db import models
from django.utils.text import slugify
from django.apps import apps


class Category(models.Model):
    name = models.CharField(max_length=55)
    slug = models.SlugField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


def brand_uploader(inst, filename):
    return f"brands/{slugify(inst.name)}.{get_ext(filename)}"


class Brand(models.Model):
    name = models.CharField(max_length=55)
    slug = models.SlugField(blank=True)
    logo = models.ImageField(upload_to=brand_uploader)

    def __str__(self) -> str:
        return self.name


class Dimension(models.Model):
    #  DIFFERENT DEPENDING ON THE PRODUCT
    length = models.FloatField(blank=True)
    breadth = models.FloatField(blank=True)
    width = models.FloatField(blank=True)
    thickness = models.FloatField(blank=True)
    diameter = models.FloatField(blank=True)

    size_in_standard_unit = models.FloatField(blank=True)
    size_in_other_unit = models.FloatField(blank=True)


class Color(models.Model):
    color = models.CharField(max_length=6)
    opacity = models.FloatField(default=1.0)


def product_main_uploader(inst, filename):
    return f"product/{slugify(inst.name)}/main.{get_ext(filename)}"


def product_thumbnail_uploader(inst, filename):
    return f"product/{slugify(inst.name)}/thumbnail.{get_ext(filename)}"


class Product(models.Model):
    # NAMING #
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    # PHOTOGRAPHS
    main_image = models.ImageField(upload_to=product_main_uploader)
    thumbnail_image = models.ImageField(
        upload_to=product_thumbnail_uploader, blank=True
    )

    # WEBSITE CONTROLS
    is_active = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)

    # ECONOMICS #
    base_price = models.FloatField()
    sale_price = models.FloatField()

    def profit_percentage(self):
        return (self.sale_price / self.base_price) * 100

    sale_percentage = models.FloatField(blank=True, null=True)

    # STATS
    sold = models.PositiveIntegerField(default=0)

    # FEEDBACK
    reviews = models.ManyToManyField(to="feedback.Review")

    def total_price(self):
        total = 0
        base = self.base_price * (self.profit_percentage / 100)
        if self.on_sale:
            total = base - (self.sale_percentage / 100) * base
        else:
            total = base

        return total

    def total_rating(self):
        return self.reviews.all().count()

    def rating(self):
        total_rating_sum = 0
        total_ratings = self.reviews.all().count()

        for rev in self.reviews.all():
            total_rating_sum += rev.rating

        return total_rating_sum / total_ratings

    # PHYSICAL FEATURES #
    dimensions = models.ForeignKey(
        to=Dimension, on_delete=models.CASCADE, blank=True, null=True
    )
    colors = models.ManyToManyField(to=Color, blank=True)

    # CATEGORIZATION #
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE)


def product_image_uploader(inst, filename):
    return f"product/{slugify(inst.name)}/{ProductImage.objects.filter(product__pk=inst.pk).count()}.{get_ext(filename)}"


def product_batch_uploader(inst, filename):
    return f"product/{slugify(inst.name)}/{slugify(inst.product.name)}/{apps.get_model(app_label='inventory', model_name='ProductImage').objects.filter(product__pk=inst.pk).count()}.{get_ext(filename)}"


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CharField)
    image = models.ImageField(upload_to=product_batch_uploader)

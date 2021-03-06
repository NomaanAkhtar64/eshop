# from inventory.utils import make_thumbnail_field, resize_image, safe_delete
from inventory.utils import compress_and_resize_image, safe_delete
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from django.utils.text import slugify
from .models import Brand, Category, Product, ProductImage


def slugify_from_name(sender, instance: Category or Brand or Product, **kw):
    if instance.slug:
        old = sender.objects.get(pk=instance.pk)
        if old.name != instance.name or old.name:
            instance.slug = slugify(instance.name)
    else:
        instance.slug = slugify(instance.name)


for model in [Category, Brand, Product]:
    pre_save.connect(slugify_from_name, sender=model)


# @receiver(post_save, sender=Brand)
# def compress_brand_logo(sender, instance: Brand, **kw):
#     # if instance.pk:
#     #     old: Brand = sender.objects.get(pk=instance.pk)
#     #     if old.logo != instance.logo:
#     #         resize_image((500, 500), instance.logo)
#     # else:

#     instance.logo = resize_image((500, 500), instance.logo)


# @receiver(post_delete, sender=Brand)
# def cleanup_brand_logo(sender, instance: Brand, **kw):
#     safe_delete(instance.logo.path)


@receiver(pre_save, sender=Brand)
def compress_brand_logo(sender, instance: Brand, **kw):
    instance.logo.save(
        *compress_and_resize_image(instance.logo, (500, 500)), save=False
    )


@receiver(post_delete, sender=Brand)
def cleanup_logo(sender, instance: Brand, **kw):
    safe_delete(instance.logo.path)
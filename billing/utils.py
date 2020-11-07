from .models import OrderItem


def get_product_revenue(self):
    total = 0
    for i in OrderItem.objects.filter(product__pk=self.pk):
        total += self.total_price() * i.quantity
    return total

from django.db import models


class OrderItem(models.Model):
    product = models.ForeignKey(to="inventory.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.total_price * self.quantity

ORDER_STATUS = [
    (1, "Placed"),
    (2, "Confirmed"),
    (3, "Canceled"),
    (4, "Shipped Off"),
    (5, "Recieved"),
]


class Order(models.Model):
    items = models.ManyToManyField(to=OrderItem)
    status = models.CharField(choices=ORDER_STATUS, max_length=32)
    is_payed = models.BooleanField(default=False)

    def base_total(self):
        total = 0
        for item in self.items.all():
            total += item.total_price()
        
        return total
    
    def calculate_shipping(self):
        #  CALCULATION GOES HERE
        return 100
    
    def grand_total(self):
        return self.base_total() + self.calculate_shipping()
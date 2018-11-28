from django.conf import settings
from django.db import models
from django.db.models import F, FloatField, Sum


from products.models import Product


class Cart(models.Model):
    promo_code = models.CharField(default='', max_length=50, blank=True)

    @property
    def total(self):
        total = self.orderitem_set.select_related('product').aggregate(
            total=Sum(F('quantity') * F('product__price'), output_field=FloatField()))['total']
        if total:
            discount = settings.PROMO_CODES.get(self.promo_code, 0)
            return '{0:.2f}'.format(total*(1-discount/100))
        return 0


class Order(models.Model):
    email = models.EmailField()
    promotion_code = models.CharField(max_length=10)
    total = models.FloatField()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, blank=True, null=True)

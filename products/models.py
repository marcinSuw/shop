from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    price = models.FloatField()
    description = models.TextField(max_length=300, blank=True, null=True)
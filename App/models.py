from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Contact(models.Model):
    full_name = models.CharField(max_length=400)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self) -> str:
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=400)
    category = models.CharField(max_length=400)
    price = models.FloatField()
    description = models.TextField()
    supplier = models.CharField(max_length=400)
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    def formatted_date(self):
        return self.date_added.strftime("%Y-%m-%d") if self.date_added else ''


class Stock(models.Model):
    product = models.CharField(max_length=400)
    current_stock = models.IntegerField()
    min_stock_level = models.IntegerField()
    max_stock_level = models.IntegerField()
    reorder_quantity = models.IntegerField()
    last_restocked = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product}"

    def formatted_date(self):
        return self.last_restocked.strftime("%Y-%m-%d") if self.last_restocked else ''


class Category(models.Model):
    cateogry = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.cateogry

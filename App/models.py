from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    full_name = models.CharField(max_length=400, verbose_name=_("Full Name"))
    email = models.EmailField(verbose_name=_("Email"))
    message = models.TextField(verbose_name=_("Message"))

    class Meta:
        verbose_name_plural = _("Contacts")

    def __str__(self) -> str:
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=400, verbose_name=_("Name"))
    category = models.CharField(max_length=400, verbose_name=_("Category"))
    price = models.FloatField(verbose_name=_("Price"))
    description = models.TextField(verbose_name=_("Description"))
    supplier = models.CharField(max_length=400, verbose_name=_("Supplier"))
    date_added = models.DateField(auto_now_add=True, verbose_name=_("Date Added"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))

    class Meta:
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return self.name

    def formatted_date(self):
        return self.date_added.strftime("%Y-%m-%d") if self.date_added else ''


class Stock(models.Model):
    product = models.CharField(max_length=400, verbose_name=_("Product"))
    current_stock = models.IntegerField(verbose_name=_("Current Stock"))
    min_stock_level = models.IntegerField(verbose_name=_("Minimum Stock Level"))
    max_stock_level = models.IntegerField(verbose_name=_("Maximum Stock Level"))
    reorder_quantity = models.IntegerField(verbose_name=_("Reorder Quantity"))
    last_restocked = models.DateField(verbose_name=_("Last Restocked"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))

    class Meta:
        verbose_name_plural = _("Stocks")

    def __str__(self) -> str:
        return f"{self.product}"

    def formatted_date(self):
        return self.last_restocked.strftime("%Y-%m-%d") if self.last_restocked else ''


class Category(models.Model):
    cateogry = models.CharField(max_length=100, verbose_name=_("Category"))
    description = models.TextField(verbose_name=_("Description"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.cateogry

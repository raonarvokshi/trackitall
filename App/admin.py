from django.contrib import admin
from .models import Contact, Product, Stock, Category


class ProductAdmin(admin.ModelAdmin):
    list_filter = ["name", "category"]
    search_fields = ("name", "category",)


admin.site.register(Product, ProductAdmin)
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin Panel"

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from App.views import *

admin.site.index_title = "Admin Panel"

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("account/", account, name="account"),
    path("account/change/password/", change_password, name="change_password"),
    path("delete/account/", delete_account, name="delete_account"),
    path("products/", products, name="products"),
    path("add-product/", add_product, name="add_product"),
    path("edit-product/<int:product_id>/", edit_product, name="edit_product"),
    path("delete-product/<int:product_id>/",
         delete_product, name="delete_product"),
    path("products/dashboard/", products_dashboard, name="products_dashboard"),
    path("stocks/", stock, name="stocks"),
    path("add-stock/", add_stock, name="add_stock"),
    path('get_product_details_by_id/<int:product_id>/',
         get_product_details_by_id, name='get_product_details_by_id'),
    path('get_product_details_by_name/<str:product_name>/',
         get_product_details_by_name, name='get_product_details_by_name'),
    path("edit-stock/<int:stock_id>/", edit_stock, name="edit_stock"),
    path("delete-stock/<int:stock_id>/", delete_stock, name="delete_stock"),
    path("stocks/dashboard/", stocks_dashboard, name="stocks_dashboard"),
    path("add-category/", add_category, name="add_category")
]

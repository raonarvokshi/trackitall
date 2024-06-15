from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Stock, Product, Contact, Category
from datetime import datetime


def redirect_if_authenticated(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already loged in")
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def redirect_if_not_authenticated(view_func):
    def _wrapped_view(request, *args, **kwargs):
        expired_session_message = 'The session has expired. Please login again to continue.'
        if expired_session_message in [msg.message for msg in messages.get_messages(request)]:
            messages.info(request, expired_session_message)
            return redirect("login")

        if not request.user.is_authenticated:
            messages.error(request, "You need to login first!")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def home(request):
    date = datetime.now()
    current_year = date.year
    context = {"current_year": current_year}

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        new_contact = Contact()
        new_contact.full_name = full_name
        new_contact.email = email
        new_contact.message = message
        new_contact.save()

        messages.success(request, "Your message was sent successfully!")
        return redirect("home")

    return render(request, "index.html", context)


@redirect_if_authenticated
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email)

        if username_exists and email_exists:
            messages.error(request, "Username and Email Already Exists!")
            return redirect("register")
        elif username_exists:
            messages.error(request, "Username Already Exists!")
            return redirect("register")
        elif email_exists:
            messages.error(request, "Email Already Exists!")
            return redirect("register")
        else:
            new_user = User.objects.create_user(
                username=username, email=email, password=password
            )
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()
            messages.success(
                request, "You Created Your Account Successfully! Please Confirm It By Logging In")
            return redirect("login")
    return render(request, "authentication/register.html")


@redirect_if_authenticated
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        verify_user = auth.authenticate(username=username, password=password)

        if not username and not password:
            messages.error(
                request, "Please enter you username and your password")
            return redirect("login")

        if not username:
            messages.error(request, "Please Enter your username")
            return redirect("login")

        if not password:
            messages.error(request, "Please enter your password")
            return redirect("login")

        if not verify_user:
            messages.error(request, "Incorrect Credentials")
            return redirect("login")

        auth.login(request, verify_user)
        messages.success(request, "You Logged In Successfully!")
        return redirect("home")

    return render(request, "authentication/login.html")


@redirect_if_not_authenticated
def logout(request):
    auth.logout(request)
    messages.success(request, "You Logged Out Successfully!")
    return redirect("home")


@redirect_if_not_authenticated
def account(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")

    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        if (
            user.first_name != first_name or
            user.last_name != last_name or
            user.username != username or
            user.email != email
        ):
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
            messages.success(
                request, "Your account details were updated successfully!")
            return redirect("account")

        else:
            messages.info(
                request, "No changes were made to your account details!")
            return redirect("account")

    return render(request, "accounts/account.html")


def change_password(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to login first!")
        return redirect("login")

    user_id = request.user.id
    current_user = request.user
    user_current_pass = request.POST.get("account_password")
    user_new_pass = request.POST.get("new_password")
    user_conf_new_pass = request.POST.get("confirm_new_password")

    if request.method == "POST":
        if current_user.check_password(user_current_pass):
            if user_new_pass == user_conf_new_pass:
                user = User.objects.get(id=user_id)
                user.set_password(user_conf_new_pass)
                user.save()
                messages.success(
                    request, "Your password was changed successfully! Please login with your new password")
                return redirect("login")
            else:
                messages.error(
                    request, "Please enter the same password in the two last fields")
                return redirect("change_password")
        else:
            messages.error(request, "Incorrect Password")
            return redirect("change_password")

    return render(request, "accounts/change_pass.html")


@redirect_if_not_authenticated
def delete_account(request):
    user = request.user

    if request.method == "POST":
        user_current_pass = request.POST.get("account_password")
        user_confirm_pass = request.POST.get("confirm_password")

        if user_current_pass == user_confirm_pass:
            if user.check_password(user_confirm_pass):
                delete_user = User.objects.get(id=request.user.id)
                delete_user.delete()
                auth.logout(request)
                messages.success(
                    request, "Your account was deleted successfully!")
                return redirect("home")
            else:
                messages.error(request, "Incorrect Password!")
                return redirect("delete_account")
        else:
            messages.error(
                request, "Please enter the same password in both fields")
            return redirect("delete_account")

    return render(request, "accounts/delete_acc.html")


@redirect_if_not_authenticated
def products(request):
    products = Product.objects.filter(user=request.user)
    context = {"products": products}
    return render(request, "product/products.html", context)


@redirect_if_not_authenticated
def add_product(request):
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        product_category = request.POST.get("product_category")
        product_price = request.POST.get("product_price")
        product_description = request.POST.get("product_description")
        product_supplier = request.POST.get("product_supplier")
        date_added = request.POST.get("date_added")

        new_product = Product()
        new_product.user = request.user
        new_product.name = product_name
        new_product.category = product_category
        new_product.price = product_price
        new_product.description = product_description
        new_product.supplier = product_supplier
        new_product.date_added = date_added
        new_product.save()

        messages.success(request, "Product Added Successfully!")
        return redirect("products")

    context = {"categories": categories}

    return render(request, "product/add_product.html", context)


@redirect_if_not_authenticated
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        product_category = request.POST.get("product_category")
        product_price = request.POST.get("product_price")
        product_description = request.POST.get("product_description")
        product_supplier = request.POST.get("product_supplier")
        date_added = request.POST.get("date_added")

        product.name = product_name
        product.category = product_category
        product.price = product_price
        product.description = product_description
        product.supplier = product_supplier
        product.date_added = date_added
        product.save()
        messages.success(request, "Product Updated Successfully!")
        return redirect("products")

    context = {"product": product}
    return render(request, "product/edit_product.html", context)


@redirect_if_not_authenticated
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product was deleted successfully!")
    return redirect("products")


@redirect_if_not_authenticated
def products_dashboard(request):
    products = Product.objects.filter(user=request.user)
    context = {"products": products}
    return render(request, "product/dashboard.html", context)


@redirect_if_not_authenticated
def stock(request):
    stocks = Stock.objects.filter(user=request.user)
    context = {"stocks": stocks}
    return render(request, "stock/stocks.html", context)


@redirect_if_not_authenticated
def add_stock(request):
    products = Product.objects.filter(user=request.user)
    if not products:
        messages.error(
            request, "First You Need To Add New Product Than The Stock For That Product")
        return redirect("add_product")

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product_name = request.POST.get("product_name")
        current_stock = request.POST.get("current_stock")
        min_stock_level = request.POST.get("min_stock_level")
        max_stock_level = request.POST.get("max_stock_level")
        reorder_quantity = request.POST.get("reorder_quantity")
        last_restocked = request.POST.get("last_restocked")

        new_stock = Stock()
        new_stock.user = request.user
        new_stock.product = product_name
        new_stock.current_stock = current_stock
        new_stock.min_stock_level = min_stock_level
        new_stock.max_stock_level = max_stock_level
        new_stock.reorder_quantity = reorder_quantity
        new_stock.last_restocked = last_restocked
        new_stock.save()

        messages.success(request, "Stock Added Successfully!")
        return redirect("stocks")

    context = {"products": products}
    return render(request, "stock/add_stock.html", context)


@redirect_if_not_authenticated
def get_product_details_by_id(request, product_id):
    product = Product.objects.get(id=product_id)
    return JsonResponse({"name": product.name})


@redirect_if_not_authenticated
def get_product_details_by_name(request, product_name):
    product = Product.objects.get(name=product_name)
    return JsonResponse({"id": product.id})


@redirect_if_not_authenticated
def edit_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product_name = request.POST.get("product_name")
        current_stock = request.POST.get("current_stock")
        min_stock_level = request.POST.get("min_stock_level")
        max_stock_level = request.POST.get("max_stock_level")
        reorder_quantity = request.POST.get("reorder_quantity")
        last_restocked = request.POST.get("last_restocked")

        stock.product_id = product_id
        stock.product_name = product_name
        stock.current_stock = current_stock
        stock.min_stock_level = min_stock_level
        stock.max_stock_level = max_stock_level
        stock.reorder_quantity = reorder_quantity
        stock.last_restocked = last_restocked
        stock.save()

        messages.success(request, "Stock Updated Successfully!")
        return redirect("stocks")

    context = {
        "stock": stock,
        "products": products,
    }
    return render(request, "stock/edit_stock.html", context)


@redirect_if_not_authenticated
def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    stock.delete()
    messages.success(request, "Stock Deleted Successfully!")
    return redirect("stocks")


@redirect_if_not_authenticated
def stocks_dashboard(request):
    stocks = Stock.objects.filter(user=request.user)
    context = {"stocks": stocks}
    return render(request, "stock/dashboard.html", context)


@redirect_if_not_authenticated
def add_category(request):
    if request.method == "POST":
        category = request.POST.get("category")
        description = request.POST.get("description")

        new_category = Category()
        new_category.cateogry = category
        new_category.description = description
        new_category.user = request.user
        new_category.save()

        messages.success(request, "New Category Added Successfully!")
        return redirect("add_category")

    return render(request, "product/add_category.html")

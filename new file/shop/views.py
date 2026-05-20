import json
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CheckoutForm, ProfileForm, SignUpForm
from .models import CartItem, Order, OrderItem, Product


def cart_totals(user):
    items = CartItem.objects.select_related("product").filter(user=user)
    total = sum(item.subtotal for item in items)
    count = sum(item.quantity for item in items)
    return items, total, count


def cart_payload(user):
    items, total, count = cart_totals(user)
    return {
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "name": item.product.name,
                "price": float(item.product.price),
                "quantity": item.quantity,
                "subtotal": float(item.subtotal),
            }
            for item in items
        ],
        "total": float(total),
        "count": count,
    }


def home(request):
    featured_products = Product.objects.filter(featured=True)[:8]
    return render(request, "shop/home.html", {"featured_products": featured_products})


def product_list(request):
    products = Product.objects.all()
    category = request.GET.get("category", "")
    max_price = request.GET.get("max_price", "")

    if category:
        products = products.filter(category=category)
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except InvalidOperation:
            messages.warning(request, "Price filter must be a valid number.")

    return render(
        request,
        "shop/product_list.html",
        {
            "products": products,
            "categories": Product.CATEGORY_CHOICES,
            "selected_category": category,
            "max_price": max_price,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(
        request,
        "shop/product_detail.html",
        {"product": product, "related_products": related_products},
    )


@login_required
def cart(request):
    items, total, count = cart_totals(request.user)
    return render(request, "shop/cart.html", {"items": items, "total": total, "count": count})


@login_required
def checkout(request):
    items, total, count = cart_totals(request.user)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("product_list")

    initial = {
        "full_name": request.user.get_full_name(),
        "email": request.user.email,
    }
    form = CheckoutForm(request.POST or None, initial=initial)

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.user = request.user
            order.total = total
            order.status = "paid"
            order.save()
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            items.delete()
        messages.success(request, "Payment simulated successfully. Your order is confirmed.")
        return redirect("profile")

    return render(request, "shop/checkout.html", {"form": form, "items": items, "total": total})


class ShopLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome! Your account is ready.")
        return redirect("profile")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "shop/profile.html", {"form": form, "orders": orders})


def api_products(request):
    products = Product.objects.all()
    data = [
        {
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "category": product.category,
            "description": product.description,
            "price": float(product.price),
            "image_url": product.image_url,
            "stock": product.stock,
            "featured": product.featured,
        }
        for product in products
    ]
    return JsonResponse({"products": data})


@login_required
def api_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    data = [
        {
            "id": order.id,
            "total": float(order.total),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": [
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "price": float(item.price),
                }
                for item in order.items.all()
            ],
        }
        for order in orders
    ]
    return JsonResponse({"orders": data})


@require_POST
@login_required
def api_cart_add(request):
    data = json.loads(request.body or "{}")
    product = get_object_or_404(Product, id=data.get("product_id"))
    quantity = max(1, int(data.get("quantity", 1)))
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    item.quantity = quantity if created else item.quantity + quantity
    item.save()
    return JsonResponse(cart_payload(request.user))


@require_POST
@login_required
def api_cart_update(request):
    data = json.loads(request.body or "{}")
    item = get_object_or_404(CartItem, id=data.get("item_id"), user=request.user)
    quantity = int(data.get("quantity", 1))
    if quantity < 1:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    return JsonResponse(cart_payload(request.user))


@require_POST
@login_required
def api_cart_remove(request):
    data = json.loads(request.body or "{}")
    item = get_object_or_404(CartItem, id=data.get("item_id"), user=request.user)
    item.delete()
    return JsonResponse(cart_payload(request.user))

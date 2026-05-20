from .models import CartItem


def cart_summary(request):
    if not request.user.is_authenticated:
        return {"cart_count": 0}
    count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    return {"cart_count": count}

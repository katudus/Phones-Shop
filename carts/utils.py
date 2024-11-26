from carts.models import Cart


def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product') # выбираем все корзины авторизир юзера; select_related выбирает одним запросом продукты на которые ссылаются корзины

    if not request.session.session_key:
        request.session.create() # сессионнный ключ для анонимного юзера
    return Cart.objects.filter(session_key=request.session.session_key).select_related('product')
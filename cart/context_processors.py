from .cart import Cart

#context to make the cart work in all pages of the site
def cart(request):
    return {'cart': Cart(request)}
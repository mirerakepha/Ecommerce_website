from shopapp.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        #get a session key if it exists
        cart = self.session.get('session_key')

        #if == new user{no session key}then: create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        #for adding products to cart/ counting the quantity
    def __len__(self):
        return len(self.cart)

    #for viewing the items in the cart
    def get_prods(self):
        #get ids from the cart
        product_ids  = self.cart.keys()
        #look products in the database using the ids
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    # cart/cart.py
    def update(self, product_id, quantity):
        product_id = str(product_id)  # always store as string (session keys must be serializable)
        product_qty = int(quantity)

        # update cart dictionary
        self.cart[product_id] = product_qty

        self.session.modified = True
        return self.cart



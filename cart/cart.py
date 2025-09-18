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


    def cart_total(self):
        # get product ids
        product_ids = self.cart.keys()
        #lookup the keys in the product database model
        products = Product.objects.filter(id__in=product_ids)
        #get quantities
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            #convert key string into int and do math
            key = int(key)
            for product in products:
                if product.id == key:
                    #another loop to do the sale price
                    if product.on_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total





    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True


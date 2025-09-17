class Cart():
    def __init__(self, request):
        self.session = request.session

        #get a session key if it exists
        cart = self.session.get('session_key')

        #if == new user{no session key}then: create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart


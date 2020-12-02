from store.models import *


class CustomerSession():
        
    def __init__(self, request):
        self.current_session = request.session
       
    def get_value(self, key):
        if key in self.current_session:
            return self.current_session[key]
        else:
            logging.debug("'" + key + "' doesn't exists in current session")
            return None

    def get_order(self):
        order_pk = self.get_value('order_pk')
        if order_pk is not None:
            return Order.objects.get(pk=order_pk)
        else: 
            return []
        
    def get_customer(self):
        customer_pk = self.get_value('customer_pk')
        if customer_pk is not None:
            return Customer.objects.get(pk=customer_pk)
        else: 
            return None

    def update_transaction_status(self, state):
        self.current_session['transaction_state'] = state
        self.current_session['show_snackbar'] = True
        logging.debug("show snackbar is true")

from store.models import *
from .session import CustomerSession

class CustomerManager():


    def __init__(self, request):
        customer_session = CustomerSession(request)
        self.session  = customer_session.current_session
        self.customer = customer_session.get_customer()
        self.order    = customer_session.get_order()


    def is_anonymous(self):
        if self.session.get_value('customer_pk') is None: 
            return True
        else: 
            return False


    def create_customer(self):
      
        # if customer is anonymous
        if self.is_anonymous:
            new_customer = Customer.objects.create()
            new_customer.name = "Anonymous-" + str(new_customer.pk)
            new_customer.save()
            print("create_customer: " + new_customer.name )

            self.session['customer_pk'] = new_customer.pk 
            self.create_order() # create an order for the new customer
            return new_customer
        else:
            print(new_customer.name + " already exists")
            return self.customer


    def create_order(self):
        order = Order.objects.create(customer = self.customer)
        order.name = self.customer.name + " order-" + str(order.pk) + " incomplete"
        order.save()
        
        self.session['order_pk'] = order.pk
        print("create order: '" + order.name  + "'")
        return order

   
    def find_customer(self, email_address):
        known_customer = Customer.objects.get(email=email_address)
        print("customer name: " + customer.name)
        
        if known_customer is None:
            return self.customer # in that case 'self.customer' refers to an anonymous one
        else:
            self.customer.delete()
            self.customer = known_customer
            self.session['customer_pk'] = known_customer.pk
            return known_customer


    def get_or_create_stripe_customer(self):
        stripe_id = self.customer.stripe_id 

        #create if not exists
        if stripe_id is None:
            stripe_customer = stripe.Customer.create(
                email   = customer_email,
                name    = customer_name,
                source  = stripe_token
            )
            stripe_id = stripe_customer['id']
            self.customer.save()
        else:
            stripe.Customer.modify(
                stripe_id,
                email   = customer_email,
                name    = customer_name,
                source  = stripe_token  
            )
            stripe_customer = stripe.Customer.retrieve(stripe_id)
    
        return stripe_customer


    def charge_customer(self, metadata, stripe_customer):

        # create charge description
        if self.order.getCartItemNumber > 1:
            description = self.customer.name + " ordered " + str(order.getCartItemNumber) + " items" 
        else: description = self.customer.name + " ordered 1 item" 

        # add charge to stripe customer
        charge = stripe.Charge.create(  
            metadata    = metadata,
            customer    = stripe_customer,
            description = description,
            amount      = int(self.order.getCartTotal * 100),
            currency    = 'eur'
        )

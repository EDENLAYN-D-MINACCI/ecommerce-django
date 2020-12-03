from ..models import *
import stripe

def get_or_create_order(request):

    try:
        order = Order.objects.get(pk=request.session['order_pk'])
        customer = order.customer
        print("get_or_create_order, get: ", order.name)

    except Exception as e: 
        print("get_or_create_order, error:",e)
        
        # create customer
        customer = Customer.objects.create()
        customer.name = "Anonymous-" + str(customer.pk)
        customer.save()

        # create order
        order = Order.objects.create(customer=customer)
        order.name = customer.name + " order-" + str(order.pk) + " open"
        order.save()

        # save primary key to session
        request.session['order_pk'] = order.pk
        print("get_or_create_order, create:", order.name)
    
    return order


def create_order(request, customer):
        # create order
        order = Order.objects.create(customer = customer)
        order.name = customer.name + " order-" + str(order.pk) + " open"
        order.save()

        # save primary key to session
        request.session['order_pk'] = order.pk
        print("create new order:", order.name)
        return order


def get_or_create_stripe_customer(customer, stripe_token):
    stripe_id = customer.stripe_id 

    #create if not exists
    try:
        if stripe_id is None:
            stripe_customer = stripe.Customer.create(
                email   = customer.email,
                name    = customer.name,
                source  = stripe_token
            )
            customer.stripe_id = stripe_customer['id']
            customer.save()
        else:
            stripe.Customer.modify(
                stripe_id,
                email   = customer.email,
                name    = customer.name,
                source  = stripe_token  
            )
            stripe_customer = stripe.Customer.retrieve(stripe_id)
        
        return stripe_customer
    
    except Exception as e:
        print("get_or_create_stripe_customer:",e)
        


def charge_customer(order, metadata, stripe_customer):

    try:
        cart_items = order.getCartItemNumber
        customer = order.customer

        if cart_items > 0:
            # create charge description
            if cart_items > 1:
                description = customer.name + " ordered " + str(order.getCartItemNumber) + " items" 
            elif cart_items == 1: 
                description = customer.name + " ordered 1 item"

            # add charge to stripe customer
            charge = stripe.Charge.create(  
                metadata    = metadata,
                customer    = stripe_customer,
                description = description,
                amount      = int(order.getCartTotal * 100),
                currency    = 'eur'
            )
            print("charge_customer: charge created")
        else:
            print("charge_customer: cart currently empty")
    
    except Exception as e:
        print("charge_customer:",e)


# used to avoid customer duplicates
def search_match_for_email(request, anonymous_order):
    anonymous_customer = anonymous_order.customer
    registered_customer = Customer.objects.filter(email=anonymous_customer.email).first()
    print("search_match_for_email: anonymous: ", anonymous_customer.email)
    print("search_match_for_email: registered: ", registered_customer.email)
    
    if registered_customer.email is None:
        return anonymous_order, anonymous_customer
    else:
        anonymous_customer.delete()
        order = create_order(request,registered_customer)
        order.customer = registered_customer
        request.session['order_pk'] = order.pk
        return order, registered_customer




import json, datetime, logging, stripe
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from .models import *
from .customer_manager.session import CustomerSession
from .customer_manager.customer import CustomerManager
from ecommerce_sculpture.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY


  



class Context():


    def __init__(self, request, site_title):
        self.session = CustomerSession(request)
        self.context = {}
        self.context['title'] = site_title

    def add_order(self):
        order = self.session.get_order()

        if order is not None:
            self.context["order"] = order
            logging.debug("order with pk: '" + str(self.session.get_value('order_pk')) + "' added to context")
        else:
            self.context["order"] = []
            logging.debug("order not existing yet")


    def add_order_items(self):
        order = self.session.get_order()

        if order is not None:
            self.context['orderItems'] = order.orderitem_set.all() 
            logging.debug("order items added to context")
            logging.debug("details: itemNumber=" + str(order.getCartItemNumber)  + "  cartTotal=" + str(order.getCartTotal))
        else:
            self.context['orderItems'] = []
            logging.debug("order not existing yet")


    def add_transaction_state(self):
        show = self.session.get_value("show_snackbar")
        state = self.session.get_value("transaction_state")

        if show is not None and state is not None:
            if show:
                self.context['transaction_state'] = state
                logging.debug("show snackbar: is false")
            else:
                self.context['transaction_state'] = 0
        self.session.current_session['show_snackbar'] = False

    

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = STRIPE_SECRET_KEY
 
# init
site_title = "mySite"
company_email = "company@gmail.com"
default_category = ProductCategories.objects.get(category="necklace")


# home page
def store(request):
    context = Context(request, site_title)
    context_store = context.context

    context.add_transaction_state()
    context_store["product_category"] = default_category#get_product_category(request)
    context_store["products"]  = Product.objects.all()
    context_store["product_categories"] = ProductCategories.objects.all()
    return render(request, 'store/store.html', context_store)

def cart(request):
    context = Context(request, site_title)
    context_cart = context.context

    context.add_order()
    context.add_order_items()  
    return render(request, 'store/cart.html', context_cart)

def checkout(request):
    context = Context(request, site_title)
    context_checkout = context.context

    #sfksfklsksd
    # adding stripe public key to context
    context_checkout['STRIPE_PUBLIC_KEY'] = STRIPE_PUBLIC_KEY
  
    # adding customer data to context
    customer = CustomerSession(request).get_customer()
    if customer.email is not None:
        context_checkout['loggedIn'] = True
        context_checkout['name']     = customer.name
        context_checkout['email']    = customer.email
        '''
        context_checkout['country']  = customer.country
        context_checkout['region']   = customer.region
        context_checkout['city']     = customer.city
        context_checkout['address']  = customer.address
        context_checkout['zip']      = customer.zipcode
        '''

    '''
    else:
        # adding customer location to context from current ip address

        location = scrap_location.get_location()
        logging.debug(location)
        context_checkout['country']  = location['country']
        context_checkout['region']   = location['region']
        context_checkout['city']     = location['city']
        context_checkout['zip']      = location['zip']
    '''

    # adding order data to context
    context.add_transaction_state()
    context.add_order()
    context.add_order_items()  
    return render(request, 'store/checkout.html', context_checkout)





def get_product_category(request):
    category = request.GET.get('category')
    if category is None:
        category = default_category
    return HttpResponse(category)



# call when adding or removing item from the cart
def order_update(request):

    # create customer if not existing yet
    customer_session = CustomerSession(request)
    customer_manager = CustomerManager(request)
    if customer_manager.is_anonymous: customer_manager.create_customer()
    
    # get javascript variables
    body = json.loads(request.body)
    action    = body['action']
    productId = body['productId']

    # updating order item
    product   = Product.objects.get(id=productId)
    order     = customer_session.get_order()
    orderItem, flag = OrderItem.objects.get_or_create(
        product = product, 
        order   = order,
        taken_by= customer_session.get_customer().name,
        name    = customer_session.get_customer().name + ":  order-" +  str(order.pk)
        )

    if action == 'add': orderItem.quantity += 1
    elif action == 'remove' and orderItem.quantity > 0: orderItem.quantity -= 1
   
    if orderItem.quantity == 0: orderItem.delete()
    else: orderItem.save()
        
    logging.debug(product.name + " added to cart" )
    return JsonResponse(productId + ' ' + action, safe=False)






def order_validation(request):
    logging.debug('POST: ' + str(request.POST))

    # init
    customer_manager = CustomerManager(request)
    customer   = customer_manager.customer
    order      = customer_manager.order
    
    if request.method == "POST":

        customer_name   = request.POST.get('name')
        customer_email  = request.POST.get('email')
        stripe_token    = request.POST.get('stripeToken')

        country = request.POST.get('country')
        region  = request.POST.get('region') 
        city    = request.POST.get('city')
        address = request.POST.get('address')
        zipcode = request.POST.get('zip')

        # If customer is anonymous search if his email match in the database
        if customer.stripe_id is None:
            customer = customer_manager.find_customer(customer_email)


        ''' SAVING CUSTOMER DATA TO STRIPE DASHBOARD '''
        try:

            #create stripe customer
            stripe_customer = customer_manager.get_or_create_stripe_customer()

            # create charge metadata
            metadata = {
                'country': country, 
                'region':  region, 
                'city':    city, 
                'address': address,
                'zipcode': zipcode
            }

            for item in order.orderitem_set.all():
                metadata[item.product.name] = str(item.quantity)


            # appply charge to customer
            customer_manager.charge_customer(metadata, stripe_customer)

        except Exception as e:
            #show error snackbar
            logging.debug(e)
            setTransactionState(-1)
            return checkout(request)


        else:
            ''' UPDATING DJANGO MODELS '''
            try:
                # update customer
                customer.name  = customer_name
                customer.email = customer_email
                customer.country = country
                customer.region  = region
                customer.city    = city
                customer.address = address
                customer.zipcode = zipcode
                customer.save()

                #update items
                for item in order.orderitem_set.all():
                    item.name = item.product.name + " bought by " + customer.name + ": order-" + str(order.pk)
                    item.taken_by = customer.name
                    item.save()

                #update order
                order.name = customer.name + " order-" + str(order.pk) + " completed"
                order.complete = True
                order.date_complete = datetime.datetime.now()
                order.save()

                # create new order
                logging.debug("order closed: '" + order.name + "'")
            
            except Exception as e:
                # discard last cart and create a new one if an error occurs
                logging.debug(e)
                return checkout(request)

            finally:
                # show success snackbar
                customer_manager.create_order()
                setTransactionState(1)
                return store(request)


def send_confirmation_email(customer):
    send_email(
        site_title + ' order', # subject
        'hey ' + customer.name + ', your payment has been accepted', # message
        company_email, # from
        [customer.email], # to
    )
      


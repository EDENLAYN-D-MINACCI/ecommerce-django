import ipinfo, stripe, json
from django.shortcuts import render
from .models import Product, ProductCategories
from .customer_handler.customer_manager import get_or_create_order
from .customer_handler.customer_request import get_product_category
from .customer_handler.transaction_status import get_status
from ecommerce_sculpture.settings import APP_TITLE, STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, IPINFO_KEY


# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = STRIPE_SECRET_KEY

# init

company_email = "company@gmail.com"
context_store = context_cart = context_checkout = {}
categories = ProductCategories.objects.all()

# home page
def store(request, selected_category="no-filter"):

    if selected_category == "no-filter":
        products = Product.objects.all()
        context_store["products"] = products

        if len(products) == 0:
            context_store["no_product"] = True
        else:
            context_store["no_product"] = False
    else:
        filtered_products = Product.objects.filter(category__category__contains=selected_category)
        context_store["products"] = filtered_products
        
        if len(filtered_products) == 0:
            context_store["no_product"] = True
        else:
            context_store["no_product"] = False

    context_store["title"]              = APP_TITLE
    context_store["product_categories"] = categories
    context_store["transaction_status"] = get_status(request)

    return render(request, 'store/store.html', context_store)



def cart(request):
    order = get_or_create_order(request)
    context_cart["title"] = APP_TITLE
    context_cart["order"] = order
    context_cart["orderItems"] = order.orderitem_set.all() 
    return render(request, 'store/cart.html', context_cart)



def checkout(request):
    order = get_or_create_order(request)
    customer = order.customer
    context_checkout["title"] = APP_TITLE

    # adding stripe public key to context
    context_checkout['STRIPE_PUBLIC_KEY'] = STRIPE_PUBLIC_KEY
  
    # adding customer data to context
    if customer.email is not None:
        context_checkout['loggedIn'] = True
        context_checkout['name']     = customer.name
        context_checkout['email']    = customer.email
        context_checkout['country']  = customer.country
        context_checkout['region']   = customer.region
        context_checkout['city']     = customer.city
        context_checkout['address']  = customer.address
        context_checkout['zip']      = customer.zipcode

    else:
        context_checkout['loggedIn'] = False

        # adding customer location to context from ip address
        try:
            details = ipinfo.getHandler(access_token=IPINFO_KEY).getDetails()
            print(details.all)
            context_checkout['country']  = details.country_name
            context_checkout['region']   = details.region
            context_checkout['city']     = details.city
            context_checkout['zip']      = details.postal

        except Exception as e:
            print("checkout:",e)
            context_checkout['country']  = ""
            context_checkout['region']   = ""
            context_checkout['city']     = ""
            context_checkout['zip']      = ""

    # adding order data to context
    context_checkout["transaction_status"] = get_status(request)
    context_checkout["order"] = order
    context_checkout["orderItems"] = order.orderitem_set.all() 
    return render(request, 'store/checkout.html', context_checkout)






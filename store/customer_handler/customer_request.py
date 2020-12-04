import json, datetime
from .customer_manager import *
from .transaction_status import *
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
 


# call when adding or removing item from the cart
def order_update(request):

    order = get_or_create_order(request)
    customer = order.customer

    # get javascript variables
    body = json.loads(request.body)
    action    = body['action']
    productId = body['productId']

    # updating order item
    product   = Product.objects.get(id=productId)
    orderItem, flag = OrderItem.objects.get_or_create(
        product = product, 
        order   = order,
        taken_by= customer.name,
        name    = customer.name + ": add " +  product.name  + " to cart"
        )

    if action == 'add': orderItem.quantity += 1
    elif action == 'remove' and orderItem.quantity > 0: orderItem.quantity -= 1
   
    if orderItem.quantity == 0: orderItem.delete()
    else: orderItem.save()
        
    print(product.name, " added to cart" )
    return JsonResponse(productId + ' ' + action, safe=False)



# call when the customer proceed to payment
def order_validation(request):
    print('POST: ',request.POST)

    # init
    order = get_or_create_order(request)
    customer = order.customer
    
    if request.method == "POST":

        customer_name   = request.POST.get('name')
        customer_email  = request.POST.get('email')
        stripe_token    = request.POST.get('stripeToken')

        country = request.POST.get('country')
        region  = request.POST.get('region') 
        city    = request.POST.get('city')
        address = request.POST.get('address')
        zipcode = request.POST.get('zip')


        # If customer is anonymous search if the typed email match in the database
        if customer.stripe_id is None:
            order, customer = search_match_for_email(request, order)


        try:

            ''' UPDATING DJANGO MODELS '''
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
                item.name = customer.name + ": bought " +  item.product.name
                item.taken_by = customer.name
                item.save()


            ''' SAVING CUSTOMER DATA TO STRIPE DASHBOARD '''
            #create stripe customer
            stripe_customer = get_or_create_stripe_customer(customer, stripe_token)

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
            charge_customer(order, metadata, stripe_customer)

        except Exception as e:
            #show error snackbar
            print("payment failed:",e)
            set_status(request,-1)
            return redirect('checkout',permanent=True)

        else:
            #update order
            order.name = customer.name + " order-" + str(order.pk) + " closed"
            order.complete = True
            order.date_complete = datetime.datetime.now()
            order.save()
            print(order.name)

            # create new order
            create_order(request, customer)

            # show success snackbar
            set_status(request,1)
            return redirect('store',permanent=True)


def send_confirmation_email():
    send_email(
        site_title + ' order', # subject
        'hey ' + customer.name + ', your payment has been accepted', # message
        company_email, # from
        [customer.email], # to
    )
      
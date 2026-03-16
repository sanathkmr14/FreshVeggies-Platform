from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.views import View
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    CustomerContact,
    UserProfile
)
from .forms import CustomerRegistrationForm, CustomerProfileForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from decimal import Decimal

# Create your views here.


class ProductView(View):
    def get(self, request):
        totalitem = 0
        products = Product.objects.all()

        data = {
            "products": products,
            "totalitem": totalitem,
        }

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        
        data["totalitem"] = totalitem

        return render(request, 'home.html', data)


#def product_detail(request):
    #return render(request, 'productdetail.html')
 
class ProductDetailView(View):
  def get(self,request,pk):
   totalitem = 0
   product = get_object_or_404(Product, pk=pk)
   item_already_in_cart = False
   if request.user.is_authenticated:
    totalitem = Cart.objects.filter(user=request.user).count()
    item_already_in_cart = Cart.objects.filter(product=product, user=request.user).exists()

   return render(request, 'productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required
def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = get_object_or_404(Product, id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart/')

@login_required
def show_cart(request):
  totalitem = Cart.objects.filter(user=request.user).count()
  user = request.user
  cart = Cart.objects.filter(user=user)
  
  if cart.exists():
    amount = 0.0
    shipping_amount = 70.0
    for p in cart:
      amount += (p.quantity * p.product.discounted_price)
    
    totalamount = amount + shipping_amount
    return render(request, 'addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount, 'totalitem': totalitem})
  else:
    return render(request, 'emptycart.html', {'totalitem':0})
   
@login_required
def plus_cart(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id')
    c = get_object_or_404(Cart, product_id=prod_id, user=request.user)
    c.quantity += 1
    c.save()
    
    amount = 0.0
    shipping_amount = 70.0
    cart_products = Cart.objects.filter(user=request.user)
  
    for p in cart_products:
     amount += (p.quantity * p.product.discounted_price)

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount
     }
    return JsonResponse(data)
  
@login_required
def minus_cart(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id')
    c = get_object_or_404(Cart, product_id=prod_id, user=request.user)
    c.quantity -= 1
    c.save()
    
    amount = 0.0
    shipping_amount = 70.0
    cart_products = Cart.objects.filter(user=request.user)
  
    for p in cart_products:
     amount += (p.quantity * p.product.discounted_price)

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount
     }
    return JsonResponse(data)
  

@login_required
def remove_cart(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id')
    c = get_object_or_404(Cart, product_id=prod_id, user=request.user)
    c.delete()
    
    amount = 0.0
    shipping_amount = 70.0
    cart_products = Cart.objects.filter(user=request.user)
  
    for p in cart_products:
     amount += (p.quantity * p.product.discounted_price)

    data = {
      'amount': amount,
      'totalamount': amount + shipping_amount,
      'cart_count': cart_products.count()
     }
    return JsonResponse(data)


@login_required
def buy_now(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = get_object_or_404(Product, id=product_id)
 # Add to cart if not already there
 item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=user)).exists()
 if not item_already_in_cart:
  Cart(user=user, product=product).save()
 return redirect('checkout')

#def login(request):
 #return render(request, 'login.html')

#def profile(request):
 #return render(request, 'profile.html')

@login_required
def address(request):
 totalitem=0
 add=Customer.objects.filter(user=request.user)
 totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'address.html', {'add':add,'active':'btn-primary', 'totalitem':totalitem})

#def passwordchange(request):
 #return render(request, 'passwordchange.html')

#def customerregistration(request):
 #return render(request, 'customerregistration.html')

class CustomerRegistrationView(View):
 def get(self,request):
  form=CustomerRegistrationForm()
  return render(request, 'customerregistration.html', {'form':form})
 def post(self,request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   form.save()
   messages.success(request, 'Registered Successfully! Please log in to continue.')
   return redirect('login')
  return render(request, 'customerregistration.html', {'form':form})
 

   

@login_required
def checkout(request):
 totalamount=0
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=70.0
 cart_products = Cart.objects.filter(user=user)
 totalitem = cart_products.count()
 if cart_products:
  for p in cart_products:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
  totalamount=amount+shipping_amount
 
 context = {
   'add': add,
   'totalamount': totalamount,
   'cart_items': cart_items,
   'totalitem': totalitem,
   'paypal_client_id': settings.PAYPAL_CLIENT_ID
 }
 
 return render(request, 'checkout.html', context)


@login_required
@csrf_exempt
def payment_done(request):
 # This view is kept for backward compatibility but is no longer used
 # PayPal payments are handled via capture_paypal_payment view
 return redirect("orders")


@login_required
@csrf_exempt
def create_paypal_payment(request):
 """Create PayPal payment order using Orders API v2"""
 if request.method == 'POST':
  try:
   data = json.loads(request.body)
   custid = data.get('custid')
   
   if not custid:
     return JsonResponse({'error': 'Customer ID is required'}, status=400)
   
   # Calculate total amount
   user = request.user
   cart_products = Cart.objects.filter(user=user)
   
   if not cart_products:
     return JsonResponse({'error': 'Cart is empty'}, status=400)
   
   amount = 0.0
   shipping_amount = 70.0
   
   for p in cart_products:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount
   
   totalamount = amount + shipping_amount
   
   # Convert to USD (PayPal REST API Orders v2 only supports specific currencies)
   # Supported currencies: USD, EUR, GBP, AUD, JPY, CAD, CHF, HKD, SGD, SEK, AUD, NZD, etc.
   # INR is NOT supported via REST Orders API
   amount_usd = round(totalamount / 83, 2)
   
   # PayPal API endpoint
   if settings.PAYPAL_MODE == 'sandbox':
     base_url = 'https://api-m.sandbox.paypal.com'
   else:
     base_url = 'https://api-m.paypal.com'
   
   # Get access token
   auth_response = requests.post(
     f'{base_url}/v1/oauth2/token',
     headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
     auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
     data={'grant_type': 'client_credentials'}
   )
   
   if auth_response.status_code != 200:
     return JsonResponse({'error': 'PayPal authentication failed'}, status=500)
   
   access_token = auth_response.json()['access_token']
   
   # Create order with USD (only supported currency for REST Orders API)
   order_payload = {
     'intent': 'CAPTURE',
     'purchase_units': [{
       'amount': {
         'currency_code': 'USD',
         'value': f"{amount_usd:.2f}"
       }
     }],
     'application_context': {
       'return_url': request.build_absolute_uri('/capture-paypal-payment/'),
       'cancel_url': request.build_absolute_uri('/checkout/'),
       'shipping_preference': 'NO_SHIPPING'
     }
   }
   
   print(f"PayPal Order Payload (USD): {order_payload}")
   
   order_response = requests.post(
     f'{base_url}/v2/checkout/orders',
     headers={
       'Content-Type': 'application/json',
       'Authorization': f'Bearer {access_token}'
     },
     json=order_payload
   )
   
   if order_response.status_code == 201:
     order_data = order_response.json()
     # Store custid in session
     request.session['paypal_custid'] = custid
     print(f"PayPal Order Created Successfully: {order_data.get('id')}")
     return JsonResponse({'id': order_data['id']})
   else:
     error_data = order_response.json()
     error_msg = error_data.get('message', 'Unknown error')
     details = error_data.get('details', [])
     print(f"PayPal Order Creation Error Status: {order_response.status_code}")
     print(f"PayPal Order Creation Error: {error_msg}")
     print(f"PayPal Details: {details}")
     print(f"Full PayPal Response: {error_data}")
     return JsonResponse({'error': f"Order creation failed: {error_msg}"}, status=400)
     
  except Exception as e:
   return JsonResponse({'error': str(e)}, status=500)
 
 return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
@csrf_exempt
def capture_paypal_payment(request):
 """Capture and verify PayPal payment using Orders API v2"""
 if request.method == 'POST':
  try:
   data = json.loads(request.body)
   order_id = data.get('orderID')
   custid = data.get('custid')
   
   if not order_id or not custid:
     return JsonResponse({'success': False, 'error': 'Missing required parameters'}, status=400)
   
   # PayPal API endpoint
   if settings.PAYPAL_MODE == 'sandbox':
     base_url = 'https://api-m.sandbox.paypal.com'
   else:
     base_url = 'https://api-m.paypal.com'
   
   # Get access token
   auth_response = requests.post(
     f'{base_url}/v1/oauth2/token',
     headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
     auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
     data={'grant_type': 'client_credentials'}
   )
   
   if auth_response.status_code != 200:
     return JsonResponse({'success': False, 'error': 'PayPal authentication failed'}, status=500)
   
   access_token = auth_response.json()['access_token']
   
   # Capture the order
   capture_response = requests.post(
     f'{base_url}/v2/checkout/orders/{order_id}/capture',
     headers={
       'Content-Type': 'application/json',
       'Authorization': f'Bearer {access_token}'
     }
   )
   
   if capture_response.status_code == 201:
     capture_data = capture_response.json()
     
     # Verify payment was completed
     if capture_data.get('status') == 'COMPLETED':
       # Payment successful - create orders
       user = request.user
       customer = Customer.objects.get(id=custid)
       cart = Cart.objects.filter(user=user)
       
       for c in cart:
         OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
         c.delete()
       
       # Clear session data
       if 'paypal_custid' in request.session:
         del request.session['paypal_custid']
       
       messages.success(request, 'PayPal payment successful! Your order has been placed.')
       return JsonResponse({'success': True})
     else:
       return JsonResponse({'success': False, 'error': 'Payment not completed'}, status=400)
   else:
     error_data = capture_response.json()
     error_message = error_data.get('message', 'Payment capture failed')
     return JsonResponse({'success': False, 'error': error_message}, status=400)
     
  except Customer.DoesNotExist:
   return JsonResponse({'success': False, 'error': 'Customer not found'}, status=404)
  except Exception as e:
   return JsonResponse({'success': False, 'error': str(e)}, status=500)
 
 return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
 


@login_required
def orders(request):
 totalitem=0
 op=OrderPlaced.objects.filter(user=request.user)
 totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'orders.html', {'order_placed':op, 'totalitem':totalitem})



@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
   totalitem=0
   if request.user.is_authenticated:
       totalitem = len(Cart.objects.filter(user=request.user))
   profile = UserProfile.objects.filter(user=request.user).first()
   if not profile:
       profile = UserProfile.objects.create(user=request.user)
   user_form = UserUpdateForm(instance=request.user, prefix='user')
   profile_form = UserProfileUpdateForm(initial={'phone': profile.phone}, prefix='profile')
   return render(request, 'profile.html', {'user_form':user_form, 'profile_form':profile_form, 'active':'btn-primary', 'totalitem':totalitem})
  
  def post(self, request):
    totalitem = Cart.objects.filter(user=request.user).count()
    profile = UserProfile.objects.filter(user=request.user).first()
    if not profile:
        profile = UserProfile.objects.create(user=request.user)
    user_form = UserUpdateForm(request.POST, instance=request.user, prefix='user')
    profile_form = UserProfileUpdateForm(request.POST, prefix='profile')
    
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      UserProfile.objects.filter(user=request.user).update(phone=profile_form.cleaned_data['phone'])
      messages.success(request, 'Congratulations! Profile Updated Successfully.')
      return redirect('profile')
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form, 'active': 'btn-primary', 'totalitem': totalitem})

@method_decorator(login_required, name='dispatch')
class AddAddressView(View):
  def get(self, request):
   totalitem=0
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   form = CustomerProfileForm()
   return render(request, 'add_address.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
  
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      usr=request.user
      name=form.cleaned_data['name']
      address=form.cleaned_data['address']
      city=form.cleaned_data['city']
      state=form.cleaned_data['state']
      zipcode=form.cleaned_data['zipcode']
      reg=Customer(user=usr,name=name, address=address, city=city, state=state, zipcode=zipcode)
      reg.save()
      messages.success(request,'Address Added Successfully!')
      return redirect('address')
    return render(request, 'add_address.html', {'form':form, 'active':'btn-primary', 'totalitem': totalitem})
  
@method_decorator(login_required, name='dispatch')
class UpdateAddressView(View):
  def get(self, request, pk):
   totalitem=0
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   add = Customer.objects.get(pk=pk)
   if add.user != request.user:
      messages.error(request, 'Unauthorized access.')
      return redirect('address')
   form = CustomerProfileForm(instance=add)
   return render(request, 'add_address.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem, 'update':True})
  
  def post(self,request, pk):
    totalitem=0
    if request.user.is_authenticated:
      totalitem = Cart.objects.filter(user=request.user).count()
    add = get_object_or_404(Customer, pk=pk)
    if add.user != request.user:
      messages.error(request, 'Unauthorized access.')
      return redirect('address')
    form = CustomerProfileForm(request.POST, instance=add)
    if form.is_valid():
      form.save()
      messages.success(request,'Address Updated Successfully..!')
      return redirect('address')
    return render(request, 'add_address.html', {'form':form, 'active':'btn-primary', 'update':True, 'totalitem': totalitem})

@login_required
def delete_address(request, pk):
    add = get_object_or_404(Customer, pk=pk)
    if add.user == request.user:
        add.delete()
        messages.success(request, 'Address Deleted Successfully!')
    else:
        messages.error(request, 'Unauthorized access.')
    return redirect('address')

@login_required
def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = CustomerContact(name=name, email=email, phone=phone, desc=message, date=timezone.now().date())
        contact.save()

        # Send Email Notification
        try:
            subject = f"New Contact Us Message from {name}"
            context = {
                'name': name,
                'email': email,
                'phone': phone,
                'message': message,
                'date': timezone.now().strftime('%B %d, %Y %I:%M %p')
            }
            html_message = render_to_string('email/contact_notification.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL], # Sending to self/admin
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
            # We still show success since the message is saved in DB

        messages.success(request, 'Your message has been sent successfully. We will get back to you soon!')
        return redirect('contact')

    return render(request, 'contact.html', {'totalitem': totalitem})

def search(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    query = request.GET.get('query', '')
    products = Product.objects.filter(title__icontains=query) if query else []
    
    context = {
        'products': products,
        'search_query': query,
        'totalitem': totalitem
    }
    return render(request, 'search.html', context)


@login_required
def place_order_cod(request):
    """Place order using Cash on Delivery (no payment gateway)"""
    user = request.user
    custid = request.GET.get('custid')
    
    if not custid:
        messages.warning(request, 'Please select a shipping address.')
        return redirect('checkout')
    
    try:
        customer = get_object_or_404(Customer, id=custid, user=user)
        cart = Cart.objects.filter(user=user)
        
        if not cart.exists():
            messages.warning(request, 'Your cart is empty.')
            return redirect('showcart')
        
        # Create OrderPlaced entries and clear cart
        for c in cart:
            OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
            c.delete()
        
        messages.success(request, 'Order placed successfully using Cash on Delivery!')
        return redirect('orders')
        
    except Customer.DoesNotExist:
        messages.error(request, 'Invalid address selected.')
        return redirect('checkout')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('checkout')

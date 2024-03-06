
from gettext import translation
from django.conf import settings
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from taggit.models import Tag
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from core.models import *
from core.forms import ProductReviewForm
from django.db.models import Avg, Count
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , authenticate, logout
import calendar
from django.db.models.functions import ExtractMonth
# from core.recomandation import generate_recommendations
from userauths.views import logout_view
from userauths.apps import UserauthsConfig
from userauths.forms import ProfileForm
from userauths.models import ConctactUs
from userauths.models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.shortcuts import render
from notifications.signals import notify

# Create your views here.

def index (request):
    products=Product.objects.filter(product_status='published', featured=True)
    user = request.user  # Adjust with the user's actual ID
    user_activity = UserActivity.objects.filter(user=user).order_by('-timestamp')
    if not request.session.has_key('currency'):
        request.session['currency']= settings.DEFAULT_CURRENCY
    products=Product.objects.filter(product_status='published', featured=True)
    # recommendations = generate_recommendations(user_activity)
    context={
        'products':products,
        # 'recommendations':recommendations,
    }

    return render(request, 'core/index.html', context)

def  selectcurrency(request):
    url= request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(url)

def  selectlanguage(request):
    if request.method == 'POST':
    #    cur_language = translation.get_language()
        url= request.META.get('HTTP_REFERER')
        lang = request.POST['language']
      #  translation.activate(lang)
      #  request.session[translation.LANGUAGE_SESSION_KEY]=lang
    path = request.path
    return HttpResponseRedirect('/'+lang)


def  savelangcur(request):
    url= request.META.get('HTTP_REFERER')
    user = request.user
    # language = Language.objects.get(code=request.LANGUAGE_CODE[0:2])
    profile = Profile.objects.get(user=user)
    # profile.language_id = language.id
    profile.currency_id = request.session['currency']
    profile.save()
    return HttpResponseRedirect(url)
    
def service_view (request):
    service=Service.objects.filter( service_status='published')

    context={
        'service':service
    }

    return render(request, 'core/service.html', context)

def product_list_view(request):
    products=Product.objects.filter(product_status='published')

    context={
        'products':products
    }

    return render(request, 'core/product-list.html', context)

def category_list_view(request):

    categories=Category.objects.all()

    context={
        'categories':categories
    }

    return render(request, 'core/category-list.html', context)


def category_product_list_view(request, cid):
    category=Category.objects.get(cid=cid)
    products=Product.objects.filter(product_status='published', category=category)

    context={
        'category':category,
        'products':products
    }

    return render(request, 'core/category-product-list.html', context)

def vendor_list_view(request):

    vendor=Vendor.objects.all()

    context={
        'vendor':vendor
    }

    return render(request, 'core/vendor-list.html', context)

def vendor_detail_view(request, vid):
    vendor=Vendor.objects.get(vid=vid)
    products=Product.objects.filter(product_status='published', vendor=vendor)

    context={
        'vendor':vendor,
        'products':products
    }

    return render(request, 'core/vendor-detail.html', context)

def product_detail_view(request, pid):
    product=Product.objects.get(pid=pid)
    reviews= ProductReview.objects.filter(product=product).order_by('-date')
    related_product=Product.objects.filter(category=product.category,).exclude(pid=pid)
    # product_variation = ProductVaraiant.objects.filter(product=product)
    review_form = ProductReviewForm()
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    product_image = product.product_images.all()
    UserActivity.objects.create(
        user = request.user,
        item = product
    )
    context={
        'product':product,
        # 'product_variation':product_variation,
        'product_image':product_image,
        'related_product':related_product,
        'review_form':review_form,
        'reviews':reviews,
        'average_reviews':average_reviews,
    }

    return render(request, 'core/product-detail.html', context)

def service_detail_view(request, sid):
    service=Service.objects.get(sid=sid)
    reviews= ServiceReview.objects.filter(service=service).order_by('-date')
    related_service=Service.objects.filter(category=service.category,).exclude(sid=sid)
    # product_variation = ProductVaraiant.objects.filter(product=product)
    review_form = ProductReviewForm()
    average_reviews = ServiceReview.objects.filter(service=service).aggregate(rating=Avg('rating'))

    # product_image = product.product_images.all()
    context={
        'service':service,
        # 'product_variation':product_variation,
        # 'product_image':product_image,
        'related_service':related_service,
        'review_form':review_form,
        'reviews':reviews,
        'average_reviews':average_reviews,
    }

    return render(request, 'core/service-detail.html', context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by('-id')

    tag =None

    if tag_slug:
        tag= get_object_or_404(Tag, slug=tag_slug)
        products=products.filter(tags__in=[tag])
    context = {
        'products':products,
        'tag':tag
    }
    return render(request, 'core/tag.html', context)

@login_required(login_url='sign-in')
def ajax_add_review(request, pid):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(pk=pid)
    user = request.user

    if request.method == 'POST':
        try:
            form = ProductReviewForm(request.POST)
            if form.is_valid():
                data, created = ProductReview.objects.get_or_create(
                    product=product,
                    user=user,
                    defaults={
                        'subject': form.cleaned_data['subject'],
                        'rating': form.cleaned_data['rating'],
                        'review': form.cleaned_data['review'],
                        # 'ip': request.META.get('REMOTE_ADDR'),
                    }

                )
                if not created:
                    data.subject = form.cleaned_data['subject']
                    data.rating = form.cleaned_data['rating']
                    data.review = form.cleaned_data['review']
                    data.ip = request.META.get('REMOTE_ADDR')
                    data.save()
                    messages.success(request, 'Thank you! Your review has been submitted.')
        except Product.DoesNotExist:
            messages.error(request, 'Product does not exist.')
    
    UserActivity.objects.create(
        user = request.user,
        item = product,
        rating = form.cleaned_data['rating'],

    )
    return redirect(url)

# def search_view(request):
#     query=request.GET.get('q')
#     category=request.GET.get('category')
#     type2=request.GET.get('type')
#     products = None
#     service = None
#     if type2== 'product' :
#         if category == 'all':
#             products = Product.objects.filter(title__icontains=query).order_by('-date')
#         else:
#             products = Product.objects.filter(title__icontains=query).filter(category__title=category).order_by('-date')
#     else:
#         if category == 'all':
#             service = Service.objects.filter(title__icontains=query).order_by('-date')
#         else:
#             service = Service.objects.filter(title__icontains=query).filter(category__title=category).order_by('-date')
#     context = {
#         'service':service,
#         'products':products,
#         'query':query,
#     }
#     if type2== 'product' :
#         return render(request, 'core/search.html', context)
#     else:
#         return render(request, 'core/search-service.html', context)



def search_view(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    type2 = request.GET.get('type')

    products = None
    service = None
    print('le voila',query)

    if type2 == 'product':
        products = Product.objects.filter(Q(title__icontains=query))
        if category != 'all':
            products = products.filter(Q(category__title=category))
        # if min_price:
        #     products = products.filter(Q(price__gte=min_price))
        # if max_price:
        #     products = products.filter(Q(price__lte=max_price))
        products = products.order_by('-date')
    else:
        service = Service.objects.filter(Q(title__icontains=query))
        if category != 'all':
            service = service.filter(Q(category__title=category))
        # if min_price:
        #     service = service.filter(Q(price__gte=min_price))
        # if max_price:
        #     service = service.filter(Q(price__lte=max_price))
        # service = service.order_by('-date')

    context = {
        'service': service,
        'products': products,
        'query': query,
    }

    filter_product(request, query)
    
    if type2 == 'product':
        return render(request, 'core/search.html', context)
    else:
        return render(request, 'core/search-service.html', context)

def filter_product(request, query=''):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")


    # Appliquez un filtre sur le champ 'title' en utilisant Q pour effectuer une recherche
    if query:
        products = Product.objects.filter(Q(title__icontains= query))
        print('yesssssssssssssssssssssssssssssssssssssssss'+ query)
    else:
        products = Product.objects.filter(product_status="published").order_by("-id")
        print('noooooooooooooooooooooooooooooooooooooooooooo')

    if min_price :
        products = products.filter(price__gte=min_price)
        products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})

        

# def filter_product(request):
#     query=request.GET.get('q')
#     categories = request.GET.getlist("category[]")
#     vendors = request.GET.getlist("vendor[]")
#     # products = Product.objects.all().order_by('-id')

#     min_price = request.GET['min_price']
#     max_price = request.GET['max_price']
    
#     products = Product.objects.filter(product_status="published").order_by("-id").distinct()


#     products = products.filter(price__gte = min_price)
#     products = products.filter(price__lte = max_price)
#     if Q !="" :
#        products = Product.objects.filter(Q(title__icontains=query))
#     else:
#         print('rienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrienrien')
#     if len(categories) > 0 :
        
#         products = products.filter(category__id__in = categories).distinct()

#     if len(vendors) > 0 :
#         products = products.filter(vendor__id__in = vendors).distinct()

#     data = render_to_string("core/async/product-list.html", {"products": products, 'query':query })
#     return JsonResponse({"data": data})


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'color_name':request.GET['color_name'],
        'color':request.GET['color'],
        'size':request.GET['size'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],
        'vendor':request.GET['vendor']
    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj']= cart_product
    return JsonResponse({'data':request.session['cart_data_obj'], 'totalcartitems' : len(request.session['cart_data_obj'])})

@login_required(login_url='sign-in')
def cart_view(request):

    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address1 = request.POST.get('address_line_1')
        address2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        region = request.POST.get('regions')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
            user=request.user,
            address_line_1 =address1,
            address_line_2=address2,
            city=city,
            country=country,
            region=region,
            mobile=mobile,
        )
        messages.success(request, 'Adrress added successfuly.')
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, 'core/cart.html', {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'address':address})
    else:
        # Lorsque 'cart_data_obj' n'est pas présent dans la session, le nombre total d'articles devrait être 0
        return render(request, 'core/cart.html', {'cart_data': '', 'totalcartitems': 0, 'cart_total_amount': cart_total_amount})

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for product_id, item in request.session:
    #         cart_total_amount += int(item['qty']) * float(item['price'])
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    context =render_to_string('core/async/cart-list.html', {'cart_data':request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj'])})
    return JsonResponse({'data':context,'totalcartitems': len(request.session['cart_data_obj'])})

def update_item_from_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id,item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    context =render_to_string('core/async/cart-list.html', {'cart_data':request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj'])})
    return JsonResponse({'data':context,'totalcartitems': len(request.session['cart_data_obj'])})


@login_required(login_url='sign-in')
def checkout_view (request):
    cart_total_amount = 0
    total_amount = 0
    notify.send(request.user, recipient=request.user, verb='Thank you to shop with us')
    
    if 'cart_data_obj' in request.session:

        for product_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount
        )
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderProducts.objects.create(
                # vendor=item.vendor
                order=order,
                invoice_no = 'INVOICE_NO-'+str(order.id),
                item=item['title'],
                size=item['size'],
                color_name=item['color_name'],
                color=item['color'],
                vendor=item['vendor'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total = float(item['qty']) * float(item['price'])
            )
    for vendor_name in item['vendor']:
        vendors = Vendor.objects.filter(title=vendor_name)

    host = request.get_host()
    paypal_dict={
        'business':settings.PAYPAL_RECEIVER_EMAIIL,
        'amount':cart_total_amount,
        'item_name':'order-item-no-No-'+str(order.id),
        'invoice':'INVOICE_NO-'+str(order.id),
        'current_code':'USD',
        'notify_url':'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url':'http://{}{}'.format(host, reverse('payment-completed',args=[order.oid])),
        'cancel_url':'http://{}{}'.format(host, reverse('payment-failed')),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, 'There are muptiple address, only one should be activate !')
        return redirect('cart')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email , password=password)

            if user is not None:
                login(request,user)
                messages.success(request, 'you are logged in .')
                return redirect ('checkout')
            else:
                messages.warning(request, 'user Does not exist , create an account.')
        except:
            messages.error(request, f'user with this {email} does not exist')

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, 'core/checkout.html', {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount,'paypal_payment_button':paypal_payment_button,'active_address':active_address})
    else:
        # Lorsque 'cart_data_obj' n'est pas présent dans la session, le nombre total d'articles devrait être 0
        return render(request, 'core/checkout.html', {'cart_data': '', 'totalcartitems': 0, 'cart_total_amount': cart_total_amount})

@login_required(login_url='sign-in')
def payment_completed_view(request,oid):

    del request.session['cart_data_obj']
    cart_orders_to_update = CartOrder.objects.filter(user=request.user, oid=oid)

# Update the 'paid_status' field to True for the retrieved queryset.
    cart_orders_to_update.update(paid_status=True)
    products={}
    try:
        order = CartOrder.objects.get(user=request.user, oid=oid)
        products = CartOrderProducts.objects.filter(order=order)
    except CartOrder.DoesNotExist:

        return HttpResponse("Order not found.")
    notify.send(request.user, recipient=request.user, verb='Thank you to shop with us')

    context={
        'products':products,
        'order':order
    }
    return render(request, 'core/payment-completed.html',context)


def payment_failed_view(request):
    return render(request , 'core/payment-failed.html')

def is_user_vendor(user):
    try:
        vendor_profile = Vendor.objects.get(user=user)
        return True
    except Vendor.DoesNotExist:
        return False

@login_required(login_url='sign-in')
def costumer_dashboard(request):
    user= request.user
    try:
        vendor2= Vendor.objects.get(user=user)
    except:
        vendor2={}

    status=STATUS_CHOICE
    # form = ProfileForm()
    profile = Profile.objects.get(user=request.user)
    orders_list = CartOrder.objects.filter(user=request.user).order_by('-id')
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month','count').filter(user=request.user)
    orders2 = CartOrderProducts.objects.filter(vendor=vendor2)
    vendor_profile = Profile.objects.get(user=user)
    is_vendor = is_user_vendor(user)
    month = []
    total_orders = []
    # total_order = list(filter(user, total_order))

    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])

    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address1 = request.POST.get('address_line_1')
        address2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        region = request.POST.get('regions')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
            user=request.user,
            address_line_1 =address1,
            address_line_2=address2,
            city=city,
            country=country,
            region=region,
            mobile=mobile,
        )
        messages.success(request, 'Adrress added successfuly.')
        return redirect('costumer-dashboard')

    context={
        'orders2':orders2,
        'status':status,
        'vendor_profile':vendor_profile,
        'total_orders':total_orders,
        'month':month,
        'orders':orders,
        'profile':profile,
        'orders_list':orders_list,
        'address':address,
        # 'form':form
    }
    if is_vendor:
        return render(request,'vendor/vendor_dashboard.html',context)
    else:
         return render(request,'core/dashboard.html',context)


@login_required(login_url='sign-in')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = request.user

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect(logout_view)
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect(change_profile)
        else:
            messages.error(request, 'Password does not match!')
            return redirect(change_profile)
    return redirect(request, 'costumer-dashboard')


# def change_profile(request):

#     if request.method == 'POST':
#         form = ProfileForm(request.FILES)
#


#         profileB = Profile.objects.all().get(user=request.user)
#         profileB.first_name = first_name
#         profileB.last_name = last_name
#         profileB.image = form.fields
#         request.user.username = username
#         profileB.bio = bio
#         profileB.save()
#         request.user.save()


#         messages.success(request, 'your profile was update successfuly')

#     return redirect('costumer-dashboard')



def change_profile(request):
    # Retrieve the user's profile
    profile = Profile.objects.all().get(user=request.user)
    if request.method == 'POST':
        image = request.FILES.get('image')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        bio = request.POST.get('bio')
        if image:
            profile.image = image
        request.user.username = username
        profile.first_name = first_name
        profile.last_name = last_name
        profile.bio = bio
        profile.save()
        request.user.save()
        messages.success(request, 'Your profile was updated successfully.')
        return redirect('costumer-dashboard')


    return redirect('costumer-dashboard')


def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_products = CartOrderProducts.objects.filter(order=order)
    products = Product.objects.all()

    context={
        'order_products':order_products,
        # 'orders':orders
    }
    return render(request,'core/order-detail.html', context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.all().filter(user=request.user).update(status=False)
    Address.objects.filter(id=id,user=request.user).update(status=True)
    return JsonResponse({"boolean": True})

@login_required(login_url='sign-in')
def wishlist_view(request):
    wishlist = Wishlist.objects.all().filter(user=request.user)
    context={
        'wishlist':wishlist
    }
    return render(request, 'core/wishlist.html', context)

@login_required(login_url='sign-in')
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    context = {}

    wishlist_count= Wishlist.objects.filter(product=product, user= request.user).count()
    if wishlist_count > 0:
        context={
            'bool':True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )

        context={
            'bool':True
        }

    return JsonResponse(context)

@login_required(login_url='sign-in')
def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)

    product = Wishlist.objects.get(id=pid)
    product.delete()

    context={
        'bool':True,
        'wishlist':wishlist
    }
    wishlist_json=serializers.serialize('json', wishlist)
    data = render_to_string('core/async/wishlist.html', context)
    return JsonResponse({'data':data,'wishlist':wishlist_json})

@login_required(login_url='sign-in')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('fist_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        messages.success(request,'thanks for your messages')
        ConctactUs.objects.create(
            message=message,
            subject= subject,
            user= request.user
        )
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

def seller_orders(request):
    user = request.user
    vendor2=Vendor.objects.get(user=user)
    orders_status = CartOrder.objects.all()
    orders = CartOrderProducts.objects.filter(vendor=vendor2, deleted = False)
    # orders = CartOrderProducts.objects.filter(vendor=vendor2, order__paid_satuts = True )

    context={
        'orders':orders,
    }
    return render(request, 'vendor/orders.html', context )


def update_orders(request, cpid):
    user = request.user
    vendor2=Vendor.objects.get(user=user)
    orders_status = CartOrder.objects.all()
    orders = CartOrderProducts.objects.filter(vendor=vendor2, deleted = False,  order__paid_satuts = True)
    # orders = CartOrderProducts.objects.filter(vendor=vendor2, order__paid_satuts = True )
    order_product =CartOrderProducts.objects.get(cpid=cpid)
    if request.method == 'POST':
        status = request.POST['status']
        order_product.product_status=status
        order_product.save()
    context={
        'orders':orders,
    }
    return redirect('seller-orders')

def delete_order(request,cpid):
    url = request.META.get('HTTP_REFERER')
    order_product = CartOrderProducts.objects.get(cpid=cpid)
    order_product.deleted = True
    messages.success(request, 'The orders was deleted successfully ')
    return redirect(url)

def add_product(request):
    user = request.user
    vendor2=Vendor.objects.get(user=user)
    if request.method == 'POST':
        product_title = request.POST['product_title']
        images = request.FILES.getlist('images')
        product_desc = request.POST['product_desc']
        product_spec = request.POST['product_spec']
        product_old_price = request.POST['product_old_price']
        product_price = request.POST['product_price']
        # device = request.POST['device']
        category = request.POST['category']
        product_desc = request.POST['product_desc']
        width = request.POST['width']
        height = request.POST['height']
        color = request.POST['color']
        color_name = request.POST['color_title']
        size = request.POST['size']
        weight = request.POST['Weight']
        tag = request.POST['tag']
        type2 = request.POST['type']
        # from_t= request.POST['from']
        # to_t= request.POST['to']
      
        if images:
            product_image = images[0]
        else:
            product_image='product.jpg'

        category=Category.objects.get(
            title=category
        )

        new_product = Product.objects.create(
            user=user,
            vendor=vendor2,
            image=product_image,
            title=product_title,
            description=product_desc,
            specification=product_spec,
            old_price=product_old_price,
            price=product_price,
            # device=device,
            category=category,
            type=type2,
            # to_d=to_t,
            # from_d=from_t,
        )
        for image in images:
            ProductImages.objects.create(images=image, product=new_product)
        AttributeVariation.objects.create(
            product=new_product,
            color_name=color_name,
            color=color,
            weight=weight,
            height=height,
            size=size,
            width=width
        )
        new_product.tags.add(*tag.split(','))


        messages.success(request, 'the product was added successfully')
        redirect (vendor_product)
    return render(request, 'vendor/add_product.html')


def add_service(request):
    user = request.user
    vendor2=Vendor.objects.get(user=user)
    if request.method == 'POST':
        product_title = request.POST['product_title']
        image = request.FILES.get('image')
        product_desc = request.POST['product_desc']
        product_spec = request.POST['product_spec']
        # product_old_price = request.POST['product_old_price']
        # product_price = request.POST['product_price']
        # device = request.POST['device']
        category = request.POST['category']
        product_desc = request.POST['product_desc']
        tag = request.POST['tag']
        type2 = request.POST['type']
        # from_t= request.POST['from']
        # to_t= request.POST['to']
        if image:
            product_image = image
        else:
            product_image='product.jpg'

        category=Category.objects.get(
            title=category
        )

        new_product = Service.objects.create(
            user=user,
            vendor=vendor2,
            image=product_image,
            title=product_title,
            description=product_desc,
            specification=product_spec,
            # old_price=product_old_price,
            #price=product_price,
            # device=device,
            category=category,
            type=type2,
            # to_d=to_t,
            # from_d=from_t,
        )

        new_product.tags.add(*tag.split(','))


        messages.success(request, 'the service was added successfully')
    return render(request, 'vendor/add_service.html')

def delete_product(request,pid):
    product = Product.objects.all().get(pid=pid)
    product.delete()
    messages.success(request, 'Product was deleted successfully ')
    return redirect(request.META.get('HTTP_REFERER'))

def delete_service(request,sid):
    service = Service.objects.all().get(sid=sid)
    service.delete()
    messages.success(request, 'Product was deleted successfully ')
    return redirect('shop-profile')

def delete_product_image(request, image_id):

    image = get_object_or_404(ProductImages, pk=image_id)
    image.delete()
    messages.success(request, 'Your product image was deleted successfully.')

    return redirect(request.META.get('HTTP_REFERER'))

def edit_product_image(request , pid , image_id):
    # product=Product.objects.get(pid=pid)
    image = get_object_or_404(ProductImages, pk=image_id) 
    if request.method == 'POST':
        new_image = request.FILES.get('new_image')
        if new_image:
            image.images = new_image
            image.save()    

    return redirect (request.META.get('HTTP_REFERER'))


def vendor_product(request):
    user = request.user
    vendor=Vendor.objects.get(user=user) 
    products= Product.objects.filter(vendor=vendor).order_by('-date')
    context={
        'products':products,
    }
    return render(request, 'vendor/product.html', context )

def vendor_service(request):
    user = request.user
    vendor=Vendor.objects.get(user=user)
    service=Service.objects.filter(vendor=vendor)
    context={
        'service':service,
    }
    return render(request, 'vendor/service.html', context )

def change_product(request,pid):
    product=Product.objects.get(pid=pid)
    product_image = product.product_images.all()
    user = request.user
    vendor2=Vendor.objects.get(user=user)
    if request.method == 'POST':
        product_title = request.POST['product_title']
        images = request.FILES.getlist('images')
        product_desc = request.POST['product_desc']
        product_spec = request.POST['product_spec']
        product_old_price = request.POST['product_old_price']
        product_price = request.POST['product_price']
        # device = request.POST['device']
        category = request.POST['category']
        product_desc = request.POST['product_desc']
        # width = request.POST['width']
        # height = request.POST['height']
        # color = request.POST['color']
        # color_title = request.POST['color_title']
        # size = request.POST['size']
        # weight = request.POST['Weight']
        #  tag = request.POST['tag']
        type2 = request.POST['type']
        # from_t= request.POST['from']
        # to_t= request.POST['to']

        category=Category.objects.get(
            title=category
        )
        for image in images:
            ProductImages.objects.create(images=image, product=product)
        if images:
            product.image = images[0]
        if product_title:
            product.title = product_title
        if product_old_price:
            product.old_price = product_old_price
        if product_price:
            product.price = product_price
        product.description = product_desc
        product.specification = product_spec
        # product.device = device
        product.category = category
        product.type = type2
        # product.tags.update(*tag.split(','))
        product.save()
        request.user.save()


        messages.success(request, 'Your product was updated successfully.')

        return redirect(vendor_product)
    context={'product':product,'product_image':product_image}

    return render(request,'vendor/change-product.html', context)


def change_service(request,sid):
    product=Service.objects.get(sid=sid)
    user = request.user
    vendor2=Vendor.objects.get(user=user)
    if request.method == 'POST':
        product_title = request.POST['product_title']
        image = request.FILES.get('image')
        product_desc = request.POST['product_desc']
        product_spec = request.POST['product_spec']
        product_old_price = request.POST['product_old_price']
        product_price = request.POST['product_price']
        # device = request.POST['device']
        category = request.POST['category']
        product_desc = request.POST['product_desc']
        # width = request.POST['width']
        # height = request.POST['height']
        # color = request.POST['color']
        # color_title = request.POST['color_title']
        # size = request.POST['size']
        # weight = request.POST['Weight']
        # tag = request.POST['tag']
        type2 = request.POST['type']
        # from_t= request.POST['from']
        # to_t= request.POST['to']

        category=Category.objects.get(
            title=category
        )
        if image:
            product.image = image
        product.title = product_title
        if product_price :
            product.price = product_price
        if product_old_price :
            product.old_price = product_old_price
        product.description = product_desc
        product.specification = product_spec
        # product.device = device
        product.category = category
        product.type = type2
       # product.tags.update(*tag.split(','))
        product.save()
        request.user.save()


        messages.success(request, 'Your product was updated successfully.')

        return redirect('shop-profile')
    context={'product':product,}

    return render(request,'vendor/change-service.html', context)


def seller_payement(request):
    return render(request, 'vendor/payement.html')

def seller_profile(request):
    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address2 = request.POST.get('address')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
            user=request.user,
            address=address2,
            mobile=mobile,
        )
        messages.success(request, 'Adrress added successfuly.')
        return redirect('costumer-dashboard')
    context={
        'address':address
    }
    return render(request, 'vendor/profile.html', context)


def shop_profile(request):
    user = request.user
    vendor=Vendor.objects.get(user=user)
    products=Product.objects.filter(vendor=vendor)
    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address2 = request.POST.get('address')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
            user=request.user,
            address=address2,
            mobile=mobile,
        )
        messages.success(request, 'Adrress added successfuly.')
        return redirect('costumer-dashboard')
    context={
        'vendor':vendor,
        'products':products,
        'address':address
    }
    return render(request, 'vendor/shop.html', context)

def sended_orders(request):
    status=STATUS_CHOICE
    # form = ProfileForm()
    profile = Profile.objects.get(user=request.user)
    orders_list = CartOrder.objects.filter(user=request.user).order_by('-id')
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month','count').filter(user=request.user)
    user= request.user
    vendor_profile = Profile.objects.get(user=user)
    is_vendor = is_user_vendor(user)
    month = []
    total_orders = []
    # total_order = list(filter(user, total_order))

    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])

    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address2 = request.POST.get('address')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
            user=request.user,
            address=address2,
            mobile=mobile,
        )
        messages.success(request, 'Adrress added successfuly.')
        return redirect('costumer-dashboard')

    context={
        'status':status,
        'vendor_profile':vendor_profile,
        'total_orders':total_orders,
        'month':month,
        'orders':orders,
        'profile':profile,
        'orders_list':orders_list,
        'address':address,
        # 'form':form
    }
    return render(request, 'vendor/sended-orders.html', context)


def seller_billing_address(request):
    status=STATUS_CHOICE
    # form = ProfileForm()
    profile = Profile.objects.get(user=request.user)
    orders_list = CartOrder.objects.filter(user=request.user).order_by('-id')
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month','count').filter(user=request.user)
    user= request.user
    vendor_profile = Profile.objects.get(user=user)
    is_vendor = is_user_vendor(user)
    month = []
    total_orders = []
    # total_order = list(filter(user, total_order))

    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])

    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address1 = request.POST.get('address_line_1')
        address2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        region = request.POST.get('regions')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
            user=request.user,
            address_line_1 =address1,
            address_line_2=address2,
            city=city,
            country=country,
            region=region,
            mobile=mobile,
        )
        messages.success(request, 'Adrress added successfuly.')
        return redirect('costumer-dashboard')

    context={
        'status':status,
        'vendor_profile':vendor_profile,
        'total_orders':total_orders,
        'month':month,
        'orders':orders,
        'profile':profile,
        'orders_list':orders_list,
        'address':address,
        # 'form':form
    }
    return render(request, 'vendor/billing-address.html', context)

def seller_change_profile(request):
    # Retrieve the user's profile
    profile = Profile.objects.all().get(user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        bio = request.POST.get('bio')
        if image:
            profile.image = image
        request.user.username = username
        profile.first_name = first_name
        profile.last_name = last_name
        profile.bio = bio
        profile.save()
        request.user.save()
        messages.success(request, 'Your profile was updated successfully.')
        return redirect('costumer-dashboard')
    status=STATUS_CHOICE
    # form = ProfileForm()
    profile = Profile.objects.get(user=request.user)
    orders_list = CartOrder.objects.filter(user=request.user).order_by('-id')
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month','count').filter(user=request.user)
    user= request.user
    vendor_profile = Profile.objects.get(user=user)
    is_vendor = is_user_vendor(user)
    month = []
    total_orders = []
    # total_order = list(filter(user, total_order))

    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])

    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address2 = request.POST.get('address')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
            user=request.user,
            address=address2,
            mobile=mobile,
        )
        messages.success(request, 'Adrress added successfuly.')
        return redirect('costumer-dashboard')

    context={
        'status':status,
        'vendor_profile':vendor_profile,
        'total_orders':total_orders,
        'month':month,
        'orders':orders,
        'profile':profile,
        'orders_list':orders_list,
        'address':address,
        # 'form':form
    }

    return render(request, 'vendor/change-profile.html', context)


def shop_change_profile(request):
    user= request.user
    # Retrieve the user's profile
    vendor=Vendor.objects.get(user=user)

    if request.method == 'POST':
        image = request.FILES.get('image')
        cover_image = request.FILES.get('cover_image')
        description = request.POST.get('description')
        title = request.POST.get('title')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        printerest = request.POST.get('printerest')
        youtube = request.POST.get('youtube')
        tiktok = request.POST.get('tiktok')

        if image:
            vendor.image = image
        if cover_image:
            vendor.cover_image = cover_image

        vendor.title = title
        vendor.description = description
        vendor.contact = phone
        if address:
            vendor.address = address
        if facebook :
            vendor.facebook = facebook
        if instagram:
            vendor.instagram = instagram
        if twitter:
            vendor.twitter = twitter
        if printerest :
            vendor.printerest = printerest
        if youtube:
            vendor.youtube = youtube
        if tiktok :
            vendor.tiktok = tiktok
        vendor.save()
        messages.success(request, 'Your shop informations was updated successfully.')
        return redirect('shop-change-profile')

    address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address2 = request.POST.get('address')
        mobile = request.POST.get('mobile')
        new_address = Address.objects.create(
            user=request.user,
            address=address2,
            mobile=mobile,
        )
        messages.success(request, 'Adrress added successfuly.')
        return redirect('shop-change-profile')

    context={
        'vendor':vendor,
        # 'address':address,
    }

    return render(request, 'vendor/change-shop-profile.html', context)





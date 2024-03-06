from django.shortcuts import get_object_or_404
from core.models import *
from django.db.models import Min ,Max
from userauths.models import Profile
def default(request):
    query = request.GET.get('q')
    # defaultcurr= settings.DEFAULT_CURRENCY
    # if not request.session.has_key('currency'):
    #     request.session['currency'] = settings.DEFAULT_CURRENCY
    # categories=Category.objects.all()
    # vendors=Vendor.objects.all()
    # min_max_price = Product.objects.aggregate(Min('price'), Max('price'))
    # try :
    #     address=Address.objects.get(user=request.user)
    # except:
    #     address=''
    

    # return{
    #     'vendors':vendors,
    #     'address':address,
    #     'categories':categories,
    #     'min_max_price':min_max_price,
    # }

    wishlist = 0
    categories=Category.objects.distinct()
    departement=Departement.objects.all()
    cat= Category.objects.all().filter()
    

    try:
        vendor2=Vendor.objects.get(user=request.user.id)
        orders_status = CartOrder.objects.all()
        orders = CartOrderProducts.objects.filter(vendor=vendor2, order__paid_status=True)
        notif = request.user.notifications.all()
        notif_count = notif.count()
    except:
        orders={}
        notif = 0
        notif_count = 0
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile=None
    vendors=Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        active_address = ''
    try :
        address=Address.objects.get(user=request.user)
    except:
         address=''

    try:
        wishlist = Wishlist.objects.all().filter(user=request.user)
        
    except:
         wishlist = 0
    product = Product.objects.all()
    # for p in product:
    #     in_wishlist = wishlist.exists
    cart_total_amount = 0
    try:
        if 'cart_data_obj' in request.session:
            for product_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])
    except:
        

        return {
            'query':query,
            'orders':orders,
            'cat':cat,
            'active_address':active_address,
            'profile':profile,
            'wishlist':wishlist,
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'vendors':vendors,
            'address':address,
            'categories':categories,
            'min_max_price':min_max_price,
            'departement':departement,
            'notif':notif,
            'notif_count':notif_count,

        }
    else:
        # When 'cart_data_obj' is not present in the session, the total number of items should be 0
        
        return {
            'query':query,
            'cat':cat,
            'orders':orders,
            'active_address':active_address,
            'profile':profile,
            'wishlist':wishlist,
            'cart_data': '',
            'totalcartitems': 0,
            'cart_total_amount': cart_total_amount,
            'vendors':vendors,
            'address':address,
            'categories':categories,
            'min_max_price':min_max_price,
            'departement':departement,
            'notif':notif,
            'notif_count':notif_count,

        }
from django.contrib import admin
from django.urls import include, path

from core.views import *

urlpatterns = [
    path('', index, name='Home'),
    path('products/', product_list_view, name='product-list'),
    # category
    path('category/', category_list_view, name='category-list'),
    path('category/<cid>/', category_product_list_view, name='category-product-list'),
    # vendor
    path('vendor/', vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', vendor_detail_view, name='vendor-detail'),
    path('product/<pid>/', product_detail_view, name='product-detail'),
    path('service/<sid>/', service_detail_view, name='service-detail'),
    path('service', service_view, name='service'),
    # path('product/', product_quick_view, name='product-view'),

    path('product/tag/<slug:tag_slug>/', tag_list, name='tags'),

    path('ajax-add-review/<int:pid>/',ajax_add_review ,name='ajax-add-review'),
    path('search/',search_view ,name='search'),

    path('filter-products/', filter_product ,name='filter-product'),

    path('add-to-cart/', add_to_cart ,name='add-to-cart'),

    path('delete-from-cart/', delete_item_from_cart, name='delete-from-cart'),

    path('cart/', cart_view, name='cart'),

    path('update-cart/', update_item_from_cart, name='update_cart'),

    path('checkout/',checkout_view, name='checkout'),

    path('paypal/',include('paypal.standard.ipn.urls')),


    path('payment-complete/<str:oid>',payment_completed_view, name='payment-completed'),

    path('payment-failed/',payment_failed_view, name='payment-failed'),

    path('dashboard/',costumer_dashboard, name='costumer-dashboard'),
    path('dashboard/change-passwaord',change_password, name='change-password'),
    path('dashboard/change-profile/',change_profile, name='change-profile'),

    path('dashboard/order/<int:id>',order_detail, name='order-detail'),

    path('make-default-address/',make_address_default, name='make-default'),
    
    path('wishlist/',wishlist_view, name='wishlist'),

    path('add-to-wishlist/',add_to_wishlist, name='add-to-wishlist'),


    path('remove-from-wishlist/',remove_wishlist, name='remove-from-wishlist'),

    path('contact/', contact, name='contact'),

    path('about/', about, name='about'),
    
    # path('seller-products/', seller_product, name='seller-product'),

    path('seller-orders/', seller_orders, name='seller-orders'),
    path('update-orders/<cpid>', update_orders, name='update-orders'),
    path('delete-orders/<cpid>', delete_order, name='delete-orders'),

    path('add-product/', add_product, name='add-product'),
    path('add-service/', add_service, name='add-service'),
    path('delete-product-image/<int:image_id>/', delete_product_image, name='delete_product_image'),
    path('edit-product-image/<pid>/<int:image_id>/', edit_product_image, name='edit_product_image'),

    path('change-product/<pid>', change_product, name='change-product'),
    path('change-service/<sid>', change_service, name='change-service'),

    path('seller/product/', vendor_product, name='vendor-product'),
    path('seller/service/', vendor_service, name='vendor-service'),

    path('transactions/', seller_payement, name='transactions'),
    path('delete-product/<pid>', delete_product, name='delete-product'),
    path('delete-service/<sid>', delete_service, name='delete-service'),
    
    path('seller-profile/', seller_profile, name='seller-profile'),
    path('shop-profile/', shop_profile, name='shop-profile'),
    path('sended-orders/', sended_orders, name='sended-orders'),
    path('billing-address/', seller_billing_address, name='billing-address'),
    path('seller/change-profile/', seller_change_profile, name='seller-change-profile'),
    path('seller/change-shop-profile/', shop_change_profile, name='shop-change-profile'),
    
    
]

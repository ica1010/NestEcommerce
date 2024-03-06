from django.contrib import admin
from core.models import *
# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ServiceImagesAdmin(admin.TabularInline):
    model = ServiceImages

class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImagesAdmin]
    list_display = ['vendor','title','product_image','price','featured','product_status']
    list_editable = ['product_status']

class ServiceAdmin(admin.ModelAdmin):
    inlines=[ServiceImagesAdmin]
    list_display = ['vendor','title','service_image','price','featured','service_status']
    list_editable = ['service_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']

class DepartementAdmin(admin.ModelAdmin):
    list_display = ['title','departement_image']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['title','vendor_image']


class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user','price','paid_status','order_date']

class CartOrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order','invoice_no','item','image','qty','price','total','product_status']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review','rating']

class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ['user','service','review','rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product','date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address_line_1', 'status']

# class ProductVaraiantAdmin(admin.ModelAdmin):
#     list_display = [ 'product' ,'color', 'size', 'amount_in_stock']

# class ColorAdmin(admin.ModelAdmin):
#     list_display = ['color', 'value']

class AttributeVariationAdmin(admin.ModelAdmin):
    list_display = ['product','color','color_name','weight','height','size','width',]
    list_filter = ('product','color_name','weight','height','size','width')

# class VariationAdmin(admin.ModelAdmin):
#     list_display = ('product', 'variation_category', 'variation_value')
#     list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Product,ProductAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Departement,DepartementAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderProducts,CartOrderProductsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(ServiceReview,ServiceReviewAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(AttributeVariation,AttributeVariationAdmin)
admin.site.register(Notification)
admin.site.register(UserActivity)


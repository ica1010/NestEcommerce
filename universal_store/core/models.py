from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.db.models import Avg, Count
from django.conf import settings
from notifications.models import Notification as BaseNotification
# Create your models here.

STATUS_CHOICE ={
    ('processing','Processsing'),
    ('shipped','Shipped'),
    ('delivered','Delivered'),
}

STATUS={
    ('draft','Draft'),
    ('disabled','Disabled'),
    ('rejected','Rejected'),
    ('in_review','In review'),
    ('published','Published'),
}

RATING={
    ('0',  '☆☆☆☆☆'),
    ('1',  '★☆☆☆☆'),
    ('2',  '★★☆☆☆'),
    ('3',  '★★★☆☆'),
    ('4',  '★★★★☆'),
    ('5',  '★★★★★'),
}


def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.

class Departement(models.Model):
    did= ShortUUIDField(unique=True, length=10, max_length= 20 , prefix='dep', alphabet='abcdefgh12345')
    title= models.CharField(max_length=100 , default='New departement')
    image= models.ImageField(upload_to='category', default='departement.jpg')
    categories = models.ManyToManyField('Category', related_name='categories', blank=True)
    class Meta:
        verbose_name ='Departement'
        verbose_name_plural = "Departements"

    

    def departement_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    cid= ShortUUIDField(unique=True, length=10, max_length= 20 , prefix='cat', alphabet='abcdefgh12345')
    departement = models.ForeignKey(Departement,on_delete=models.SET_NULL , null=True , related_name='departement')
    title= models.CharField(max_length=100 , default='New category')
    image= models.ImageField(upload_to='category', default='category.jpg')
    class Meta:
        verbose_name ='Category'
        verbose_name_plural = "categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title

    
class Vendor(models.Model):
    vid= ShortUUIDField(unique=True, length=10, max_length= 20 , prefix='ven', alphabet='abcdefgh12345')

    title= ShortUUIDField(unique=True, length=10, max_length= 20 , prefix='vendor', alphabet='1234567890')
    image = models.ImageField(upload_to=user_directory_path , default="./default_Profile.png")
    cover_image = models.ImageField(upload_to=user_directory_path,  default="./default_banner.png")
    description = RichTextUploadingField(null=True, blank=True, default='I am a vendor')
    
    address = models.CharField(max_length=100, default='')
    contact = PhoneNumberField()
    # contact = models.CharField(max_length=50)
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')
    facebook = models.CharField(max_length=250, default='')
    instagram = models.CharField(max_length=250, default='')
    twitter = models.CharField(max_length=250, default='')
    printerest = models.CharField(max_length=250, default='')
    youtube = models.CharField(max_length=250, default='')
    tiktok = models.CharField(max_length=250, default='')

    user = models.ForeignKey(User,on_delete=models.CASCADE , null=True)
    class Meta:
        verbose_name ='Vendor'
        verbose_name_plural = "Vendors"
    widgets = {                          
            contact: PhoneNumberPrefixWidget(attrs={"placeholder":'Phone number'}),
        }

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.cover_image.url))
    
    def __str__(self):
        return self.title

class Product(models.Model):
    pid= ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefgh12345')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL , null=True , related_name='category')
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE , null=True,related_name='vendor')
    user = models.ForeignKey(User,on_delete=models.CASCADE , null=True,blank=True)
    title= models.CharField(max_length=100, default='Untitle Product')
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = RichTextUploadingField(null=True, blank=True, default='New product')
    type = models.CharField(max_length=100, default='Untitle type', blank=True, null=True)      
    stock_count= models.IntegerField(default='0',blank=True, null=True)      
    from_d= models.DateTimeField(blank=True, null=True)      
    to_d= models.DateTimeField(auto_now_add=False,blank=True, null=True)      
    price= models.DecimalField(max_digits=999999999, decimal_places=2, default='1000.00')
    old_price= models.DecimalField(max_digits=999999999, decimal_places=2, default='1500.00')
    specification = RichTextUploadingField(null=True, blank=True)
    tags = TaggableManager(blank=True)



    product_status = models.CharField( choices=STATUS, max_length=10,default='in_review')



    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)


    sku= ShortUUIDField(unique=True, length=4, max_length= 20 ,prefix='sku', alphabet='1234567890')
    date=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name ='Product'
        verbose_name_plural = "Products"
        ordering = ('-date',)

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
        
    def __str__(self):
        return self.title
    def get_percentage(self):
        new_price= 100-(self.price/self.old_price)*100
        return new_price
    
    def averageReview(self):
        reviews = ProductReview.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ProductReview.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class ProductImages(models.Model):
    images=models.ImageField(upload_to='product-images',default='product.jpg') 
    product = models.ForeignKey(Product,on_delete=models.SET_NULL , null=True, related_name='product_images')
    date= models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Product Images'

            # color_name=color_name,
            # color=color,

            # weight=weight,
            
            # height=height,
            
            # size=size,
            
            # width=width
class AttributeVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    color = ColorField()
            # weight=weight,
            
            # height=height,
            
            # size=size,
            
            # width=width
    color_name=models.CharField(max_length=50)

    weight = models.CharField(max_length=100)

    width = models.CharField(max_length=100)
    
    height = models.CharField(max_length=100)

    size = models.CharField(max_length=100)

class Service(models.Model):
    sid= ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefgh12345')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL , null=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL , null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL , null=True)
    title= models.CharField(max_length=100, default='Untitle Service')
    image = models.ImageField(upload_to=user_directory_path, default='service.jpg')
    description = RichTextUploadingField(null=True, blank=True, default='New service')
    
    type= models.CharField(max_length=100, default='Untitle type', blank=True, null=True)

    from_this_time = models.DateTimeField(blank=True, null=True)
    to_this_time= models.DateTimeField(blank=True, null=True)
    
    price= models.DecimalField(max_digits=999999999, decimal_places=2, blank=True, null=True)
    old_price= models.DecimalField(max_digits=999999999, decimal_places=2, blank=True, null=True)
    # device = models.CharField(max_length=50 , blank=True, null=True)


    specification = RichTextUploadingField(null=True, blank=True)
    tags = TaggableManager(blank=True)

    service_status = models.CharField( choices=STATUS, max_length=10, default='in_review')

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku= ShortUUIDField(unique=True, length=4, max_length= 20 ,prefix='sku', alphabet='1234567890')

    date=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name ='Service'
        verbose_name_plural = "Services"

    def service_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
        
    def __str__(self):
        return self.title
    def get_percentage(self):
        new_price= (self.price/self.old_price)*100
        return new_price
    
    def averageReview(self):
        reviews = ServiceReview.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ServiceReview.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class CartOrder(models.Model):
    oid= ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='1234567890')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=99999999999, decimal_places=2, default='1000.00')
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Cart Order'
    def __str__(self):
       return f'{self.user.username}-{self.oid}' 

class CartOrderProducts(models.Model):
    vendor=models.CharField(max_length=200)
    cpid= ShortUUIDField(unique=True, length=4, max_length= 20 , alphabet='1234567890')
    order = models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=200)
    product_status=models.CharField(max_length=30, default='processing', choices=STATUS_CHOICE)
    item =models.CharField(max_length=200)
    image=models.CharField(max_length=200)
    color_name = models.CharField(max_length=100 ,default='')
    color =  ColorField()
    size = models.CharField(max_length=100 ,default='')
    qty = models.IntegerField(default=0)
    price= models.DecimalField(max_digits=99999999999, decimal_places=2, default='1000.00')
    total= models.DecimalField(max_digits=99999999999, decimal_places=2, default='1000.00')
    deleted = models.BooleanField(default = False)
    
    class Meta:
        verbose_name_plural = 'Cart Order Products'

class ProductReview(models.Model):    
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    review =RichTextUploadingField()
    subject = models.CharField(max_length=100, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(default='10.10.10.245')

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
       return f'{self.product.title}-{self.user.username}' 
    
    def get_rating(self):
       return self.rating

class ServiceReview(models.Model):    
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service,on_delete=models.SET_NULL, null=True)
    review =RichTextUploadingField()
    subject = models.CharField(max_length=100, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(default='10.10.10.245')

    class Meta:
        verbose_name_plural = 'Service Reviews'

    def __str__(self):
       return f'{self.service.title}-{self.user.username}' 
    
    def get_rating(self):
       return self.rating
    
class ServiceImages(models.Model):
    images=models.ImageField(upload_to='services-images',default='service.jpg') 
    service = models.ForeignKey(Service,on_delete=models.SET_NULL , null=True, related_name='service_images')
    date= models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural='Service Images'

class Wishlist(models.Model):    
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
       return self.product.title
    
class Address(models.Model):    
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    address_line_1 = models.CharField(max_length=100, null=True)
    address_line_2 = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    mobile  = PhoneNumberField(blank=True, null=True)
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'

    def __str__(self):
       return self.user.email
   
class NotificationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Notification(BaseNotification):
    receptor  = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    # Additional fields specific to your notification

    class Meta:
        ordering = ['-timestamp']


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    timestamp = models.DateField(auto_now_add=True)
    
    rating = models.PositiveIntegerField(null=True, blank=True, default = 0)

    def __str__(self):
        return f'{self.user.username} interacted with {self.item} on {self.timestamp}'
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save
from django.dispatch import receiver
from currencies.models import Currency 

# Create your models here.

class User(AbstractUser):
    id= ShortUUIDField(unique=True, length=4, max_length= 20 ,prefix='', alphabet='1234567890',primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=60)
    image= models.ImageField(upload_to='profile', default="./default_Profile.png")
    phone = PhoneNumberField()
    bio = models.TextField(default='')
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image',default="./default_Profile.png")
    first_name = models.CharField(max_length=70, null=True, blank=True, default='My firstname')
    last_name = models.CharField(max_length=70, null=True, blank=True,default='My lastname')
    bio = models.TextField(null=True, blank=True,default='Hi ,i\'am new')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    # language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True, null=True)
    verified = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.last_name
    
class ConctactUs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=250)

    class Meta:
        verbose_name='Contact US'
        verbose_name_plural='Contact US'

    def __str__(self):
        return self.user.username

# class UserActivity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     item = models.CharField(max_length=100)
#     timestamp = models.DateTimeField()
#     rating = models.PositiveIntegerField(null=True, blank=True)

#     def __str__(self):
#         return f'{self.user.username} interacted with {self.item} on {self.timestamp}'
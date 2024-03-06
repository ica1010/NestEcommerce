from django.contrib import admin
from userauths.models import *
from userauths.models import User
from django.contrib import admin
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# Register your models here


class UserAdmin(admin.ModelAdmin):
    list_display=['username', 'phone', 'email', 'bio']
    class Meta:
        widgets = {
            'phone': PhoneNumberPrefixWidget(initial='US'),
        }

class ContactUsAdmin(admin.ModelAdmin):
    list_display=['user','subject', 'message']

class ProfileAdmin(admin.ModelAdmin):
    list_display=['first_name', 'last_name', 'bio']
    
admin.site.register(User,UserAdmin)
admin.site.register(ConctactUs,ContactUsAdmin)
admin.site.register(Profile,ProfileAdmin)
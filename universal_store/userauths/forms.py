from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import Profile
from userauths.models import User
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.modelfields import PhoneNumberField
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder":'Email'}))
    phone = PhoneNumberField()
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":'confirm Password'}))
    class Meta:
        model = User
        fields = ['username', 'email','phone']
        widgets = {                          
            'phone': PhoneNumberPrefixWidget(attrs={"placeholder":'Phone number'}),
        }

class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ('image',)
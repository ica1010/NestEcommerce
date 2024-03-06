from django.conf import settings
from django.shortcuts import redirect, render
from core.admin import VendorAdmin
from core.models import Vendor
from userauths.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login , authenticate, logout
from userauths.models import User
from notifications.signals import notify

# Create your views here.

#User = settings.AUTH_USER_MODEL
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            vendor = request.POST.get('vendor')
            if vendor == 'vendor' :
                new_vendor = Vendor.objects.create(
                    user = new_user
                )
            messages.success(request, f'Wellcome {username}, your account was successfully created')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    phone=form.cleaned_data['phone']
            )
            login(request , new_user)
            notify.send(request.user, recipient=request.user, verb='Welcome to ours website,set up yours belling addess to start by product')

            return redirect('Home')
        
    else:
        form = UserRegisterForm()

    context = {
        'form':form,
    }
    return render(request, 'user/sign-up.html', context)

def login_view(request):
    url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        messages.warning(request, f'you are already logged in.')
        return redirect('Home')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email , password=password)

            if user is not None:
                login(request,user)
                messages.success(request, 'you are logged in .')
                notify.send(request.user, recipient=request.user, verb='Thank you to shop with us')

                return redirect ('Home')
            else:
                messages.warning(request, 'user Does not exist , create an account.')
        except:
            messages.error(request, f'user with this {email} does not exist')

    return render(request , 'user/sign-in.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'you are now logged out ')
    return redirect('sign-in')
from django.shortcuts import redirect, render

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from accounts_app.forms import RegistrationForm
from accounts_app.models import Account

import requests
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
             # USER ACTIVATION
            # current_site = get_current_site(request)
            # mail_subject = 'Please activate your account'
            # message = render_to_string('account/account_verification_email.html', {
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),

            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()
            # # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address . Please verify it.')
            # return redirect('/account/log_in/?command=verification&email='+email)
            
            messages.success(request, 'Registration Successful.')
            return redirect('log_in')
        
        
    else:
        form = RegistrationForm()
         
    context = {
        'form':form,
    }
    return render(request, 'account/register.html', context)



def log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in.')
            return redirect ('dashboard')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect ('log_in')
        
    return render(request, 'account/log_in.html')





@login_required(login_url = 'log_in')
def log_out(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('log_in')


# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Account._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Congratulations! Your account is activated.')
#         return redirect('login')
#     else:
#         messages.error(request, 'Invalid activation link')
#         return redirect('register')




# @login_required(login_url = 'login')
def dashboard(request):
#     orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
#     orders_count = orders.count()

#     userprofile = UserProfile.objects.get(user_id=request.user.id)
#     context = {
#         'orders_count': orders_count,
#         'userprofile': userprofile,
#     }
#     return render(request, 'account/dashboard.html', context)
    return render(request, 'account/dashboard.html')
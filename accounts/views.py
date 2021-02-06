from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import account_activation_token

User=get_user_model()
# Create your views here.
def Home(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email =request.POST.get('email')
        city =request.POST.get('city')
        fees =request.POST.get('fees')
        purpose =request.POST.get('purpose')
        User(
            email=email,first_name=first_name,last_name=last_name,city=city,register_free=fees,purpose=purpose
        ).save()
        messages.success(request,"Register Completed ,Waited for Admin Verification")
        return redirect('home')
    else:
        return render(request,'index.html')

def LoginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            if get_object_or_404(User,email=email).is_active==False:
               messages.error(request,"Account is not active")
               return redirect('login')
            else:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dash')
                else:
                    messages.error(request, "Enter correct email & password")
                    return redirect('login')

        else:
            return render(request, 'dashboard/login.html')

def Dashboard(request):
    return render(request,'dashboard/index.html')

def Logout(request):
    logout(request)
    return redirect('login')

def UserList(request):
    if request.user.is_superuser:
        user =User.objects.all()
        return render(request,'dashboard/tables.html',{'us':user})
    else:
        return HttpResponse("You not allow to this page")
import random
import string

import random
import string

def get_random_alphanumeric_string(letters_count, digits_count):
    sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))

    # Convert string to list and shuffle it to mix letters and digits
    sample_list = list(sample_str)
    random.shuffle(sample_list)
    final_string = ''.join(sample_list)
    return final_string

def Update(request,id):
    if request.method=="POST":
        user = get_object_or_404(User, id=id)
        res =request.POST.get("userc")
        if(res=="True" and user.is_active==False):
            user.is_varified = True
            user.is_active = True
            password=get_random_alphanumeric_string(6,2)
            user.set_password(password)
            mail_subject = 'Activate your  account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'pass': password,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
        elif(res=="True" and user.is_active==True):
            pass
        elif (res=="False" and user.is_active==True):
            user.is_varified = False
            user.is_active=False
        else:
            return redirect('userlist')
        user.save()
        return redirect('userlist')

def Delete(request,id):
    if request.user.is_superuser:
        user=get_object_or_404(User,id=id)
        user.delete()
        return redirect('userlist')
    else:
        return HttpResponse("You are nit llow to delete anything")

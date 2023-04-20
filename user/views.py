from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login 
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
import random
from twilio.rest import Client
from django.conf import settings

# Create your views here.
def home(request):
    return render(request, 'home.html')

def send_otp(mobile , otp):
    account_sid = 'AC1377db0737256c348fc40a77e5f15a2c'
    auth_token = '601750878cc1678442f26f36fbeddefb'
  
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                              from_='+12342316600',
                              body ='Your OTP is '+otp,
                              to ='+91'+mobile
                          )
    print(message.sid)
    return None

def register(request):
    if request.user.is_authenticated:
      return redirect("/")   
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            mobile = request.POST.get('mobile')
            otp = str(random.randint(100000, 999999))
            send_otp(mobile , otp)
            print(otp)

            request.session['username'] = username
            request.session['mobile'] = mobile
            request.session['otp'] = otp

            return redirect('/reg_otp/')

        return render(request,'register.html')
    
def reg_otp(request):
    username = request.session['username']
    mobile = request.session['mobile']
    rec_otp = request.session['otp']

    if request.method == 'POST':
        otp = request.POST.get('otp') 
        
        if otp == rec_otp:
            user =  User(username = mobile, first_name = username)
            user.set_password(None)
            user.save()
            messages.success(request, f"User Registerd successfully")
            return redirect('/login/')
        else:
            messages.warning(request, f"Wrong OTP")

    return render(request, 'otp-page.html')    
       

def login(request):
    if request.user.is_authenticated:
      return redirect("/")
    else:
        if request.method == 'POST':
            mobile = request.POST['mobile'] 
            otp = str(random.randint(100000, 999999))
            send_otp(mobile , otp)
            print(otp)

            request.session['mobile'] = mobile
            request.session['otp'] = otp
            
            return redirect('/login_otp/') 

        return render(request, "login.html")

def login_otp(request):
    mobile = request.session['mobile']
    rec_otp = request.session['otp']

    if request.method == 'POST':
        otp = request.POST.get('otp') 
        
        if otp == rec_otp:
            user =  User.objects.filter(username = mobile).first()
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back {user.first_name}")
                return redirect('/profile/')
        else:
            messages.warning(request, f"Wrong OTP")

    return render(request, 'otp-page.html') 

def logout_user(request):
	logout(request)
	return redirect("/login/")

@login_required(login_url='login')
def profile(request):
    user_id = request.user.id
    user=User.objects.filter(id=user_id).first()
    return render(request, "profile.html",{'user':user,})
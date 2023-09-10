from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User 
from django.contrib import messages

import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from six import text_type
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model, update_session_auth_hash

from django.contrib.auth.decorators import login_required

# Create your views here.


def handlesignup(request):
    print("hello")
    
    if request.method=="POST":
        uname=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")
        confirmpassword=request.POST.get("pass2")

        request.session["username"]=uname
        request.session["email"]=email
        request.session["password"]=password

        if password!=confirmpassword:
            messages.warning(request,"password is incorrect")
            return redirect('handlesignup')
        
        try:
            if User.objects.get(username=uname):
                messages.info(request,"username is taken")
                return redirect('handlesignup')
            
        except:
            pass

        try:
            if User.objects.get(email=email):
                messages.info(request,"email is taken")
                return redirect('handlesignup')
            
        except:
            pass
            send_otp(request)
            return render(request,'user/otp.html',{"email":email})


        
        myuser=User.objects.create_user(uname,email,password)
        myuser.save()
        messages.success(request,"signup is successfull  please Login")
        return redirect('handlelogin')
    
        
    return render(request,'user/signup.html')

def handlelogin(request):
    print("hii")
    if request.method=="POST":
        uname=request.POST.get("username")
        pass1=request.POST.get("pass1")
        myuser=authenticate(username=uname,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login success")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentails")
            return redirect('handlelogin')
    # if not request.user.is_authenticated:    
    #     return render(request,'home.html')
    # else:    
    return render(request,'user/login.html')

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('index')


def send_otp(request):
    s=""
    for x in range(0,4):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    send_mail("otp for signup",s,'prajithchandran08@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"user/otp.html")

def otp_verification(request):
    print("luckk")
    if request.method=='POST':
        otp = request.POST.get("otp")
    if otp == request.session["otp"]:
        encryptedpassword=make_password(request.session['password'])
        nameuser=User(username=request.session['username'],email=request.session['email'],password=encryptedpassword)
        nameuser.save()
        messages.info(request,'signed in successfully')
        User.is_active=True
        return redirect('handlelogin')
    else:
        messages.error(request,"otp doesnt match")
        return render(request,'user/otp.html')
    
@login_required
def verification(request):
    print("luckk")
    if request.method == 'POST':
        otp = request.POST.get("otp")
    
    if otp == request.session["otp"]:
        try:
            existing_user = User.objects.get(username=request.session['username'])
            existing_user.email = request.session['email']
            existing_user.password = make_password(request.session['password'])
            existing_user.save()
        except User.DoesNotExist:
            new_user = User(username=request.session['username'], email=request.session['email'], password=make_password(request.session['password']))
            new_user.save()
        
        messages.info(request, 'Signed in successfully')
        return redirect('reset_password')
    else:
        messages.error(request, "OTP doesn't match")
        return render(request, 'user/otp.html')




def forgotpassword(request):
    if request.method=="POST":
        email=request.POST.get("email")

        try:
            if User.objects.get(email=email):
                send_otp(request)
                return render(request,'user/passwordotp.html',{"email":email})
        except:
            messages.info(request,"email is wrong")
            return redirect('forgotpassword')
        

        messages.success(request,"otp entered is successfull  please enter the new password")
        return redirect('reset_password')
    return render(request, 'user/forgotpassword.html')

@login_required
def reset_password(request):
    print("hullllll")
    if request.user.is_authenticated:
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            
        if new_password:    
            # Get the currently logged in user
            user = request.user
            
            # Update the user's password
            user.set_password(new_password)
            user.save()
            
            
            # Update the session authentication hash to prevent logout
            update_session_auth_hash(request, user)
            
            # Redirect the user to a success page or another page
            return redirect('handlelogin')
    else:
        pass

    return render(request, 'user/reset_password.html')
        


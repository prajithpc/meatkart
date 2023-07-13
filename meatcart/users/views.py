from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User 
from django.contrib import messages
# Create your views here.


def handlesignup(request):
    print("hello")
    
    if request.method=="POST":
        uname=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")
        confirmpassword=request.POST.get("pass2")

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
    return redirect('handlelogin')



from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        uemail = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Passwords did not match")
        else:
            my_user = User.objects.create_user(uname, uemail, pass1)
            my_user.save()
            return redirect('mysite')

    return render(request, "Registration/signup.html")

def LoginPage(request):
    if request.method == 'POST':
        uname = request.POST.get("username")
        pass1 = request.POST.get("pass")

        user = authenticate(request, username= uname, password = pass1)

        if user is not None:
            login(request, user)
            return redirect('mysite')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, "Registration/login.html")

def LogoutPage(request):
    logout(request)
    return redirect('login')
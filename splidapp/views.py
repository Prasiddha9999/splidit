from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Login success")
            return redirect('home') 
        else:
            messages.error(request, 'Invalid Login Credentials')

    return redirect('index')  

def register_view(request):
    print("Hello love ")
    if request.method == 'POST':
        username = request.POST.get('new_username')
        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('index')  
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('index')  

        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Passwords do not match')

    return redirect('index')  

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

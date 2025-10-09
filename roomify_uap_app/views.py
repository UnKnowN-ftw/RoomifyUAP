from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return render(request, 'roomify_login_register.html')


def login_user(request, role):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('home')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in successfully as {role.capitalize()}!")

            if role == 'renter':
                return redirect('renter_dashboard')
            if role == 'owner':
                return redirect('owner_dashboard')

            return redirect('home')

        messages.error(request, 'Invalid username or password.')
        return redirect('home')

    return redirect('home')


def register_user(request, role):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        username = request.POST.get('username', '').strip()
        if not username and email:
            username = email.split('@')[0]

        if not username:
            messages.error(request, 'A username or valid email is required.')
            return redirect('home')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('home')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user.save()

        # TODO: store phone/role in a Profile model

        messages.success(request, f"Account created successfully as {role.capitalize()}! Please log in.")
        return redirect('home')

    return redirect('home')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('home')
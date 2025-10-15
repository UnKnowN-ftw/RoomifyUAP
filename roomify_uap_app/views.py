from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def home(request):
    if request.user.is_authenticated:
        # Redirect logged-in users directly to their dashboard
        profile = Profile.objects.filter(user=request.user).first()
        if profile and profile.role == 'renter':
            return redirect('renter_dashboard')
        elif profile and profile.role == 'owner':
            return redirect('owner_dashboard')
    return render(request, 'homepage.html')


def renter_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    profile = Profile.objects.filter(user=request.user).first()
    if not profile or profile.role != 'renter':
        messages.error(request, 'Access denied.')
        return redirect('home')
    return render(request, 'renter_dashboard.html')


def owner_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    profile = Profile.objects.filter(user=request.user).first()
    if not profile or profile.role != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')
    return render(request, 'owner_dashboard.html')


def login_user(request, role):
    """
    - GET: render the login form (role is 'renter' or 'owner')
    - POST: authenticate and redirect to dashboard
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Both fields are required.')
            return redirect('login_user', role=role)

        user = authenticate(request, username=username, password=password)
        if user:
            profile = Profile.objects.filter(user=user).first()
            if not profile or profile.role != role:
                messages.error(request, f'You are not registered as a {role}.')
                return redirect('login_user', role=role)

            login(request, user)
            if role == 'renter':
                return redirect('renter_dashboard')
            else:
                return redirect('owner_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login_user', role=role)

    # GET -> render the login form template
    return render(request, 'roomify_login_register.html', {'action': 'login', 'role': role})


def register_user(request, role):
    """
    - GET: render the registration form (role is 'renter' or 'owner')
    - POST: validate, create user+profile, login and redirect
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # If username empty but email provided, derive username from email
        if not username and email:
            username = email.split('@')[0]

        if not username:
            messages.error(request, 'Username or email is required.')
            return redirect('register_user', role=role)

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_user', role=role)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_user', role=role)

        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register_user', role=role)

        # Create user and profile
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        Profile.objects.create(user=user, role=role, phone=phone)

        # Auto-login
        login(request, user)
        if role == 'renter':
            return redirect('renter_dashboard')
        else:
            return redirect('owner_dashboard')

    # GET -> render the registration form template
    return render(request, 'roomify_login_register.html', {'action': 'register', 'role': role})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Logged out successfully.')
    return redirect('home')

def post_new_listing(request):
    return render(request, 'post_new_listing.html')


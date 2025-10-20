from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Listing
from .models import Owner, Renter
from .models import BookingRequest


def home(request):
    if request.user.is_authenticated:
        # Redirect logged-in users directly to their dashboard
        profile = Profile.objects.filter(user=request.user).first()
        if profile and profile.role == 'renter':
            return redirect('renter_dashboard')
        elif profile and profile.role == 'owner':
            return redirect('owner_dashboard')
    return render(request, 'homepage.html')


@login_required
def renter_dashboard(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile or profile.role != 'renter':
        messages.error(request, 'Access denied.')
        return redirect('home')

    # ✅ Show all available listings
    listings = Listing.objects.all().order_by('-created_at')

    # ✅ Notification count: only accepted/rejected responses for this renter
    notifications = BookingRequest.objects.filter(
        renter=request.user
    ).exclude(status='pending').count()

    return render(request, 'renter_dashboard.html', {
        'listings': listings,
        'notification_count': notifications
    })


@login_required
def owner_dashboard(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile or profile.role != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')

    owner_listings = Listing.objects.filter(owner=request.user).order_by('-created_at')

    notifications = BookingRequest.objects.filter(
        owner=request.user,
        status='pending'
    )

    return render(request, 'owner_dashboard.html', {
        'listings': owner_listings,
        'notification_count': notifications.count(),
        'notifications': notifications
    })


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

def admin_login(request):
    # Clear previous messages so old ones don't show on login page
    list(messages.get_messages(request))  # consumes all existing messages

    # If already logged in as staff, redirect to admin dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or unauthorized access.')

    return render(request, 'admin_login.html')


@staff_member_required(login_url='admin_login')
def admin_dashboard(request):
    owners = Owner.objects.all()
    renters = Renter.objects.all()
    admin_user = request.user  # logged-in admin
    return render(request, 'admin_dashboard.html', {
        'owners': owners,
        'renters': renters,
        'admin_user': admin_user
    })

    
@staff_member_required(login_url='admin_login')
def view_users(request):
    """Display all users with filters and actions."""
    users = User.objects.all().order_by('id')

    # Optional: filter by staff/superuser/active if GET parameters exist
    staff_filter = request.GET.get('staff', 'all')
    super_filter = request.GET.get('superuser', 'all')
    active_filter = request.GET.get('active', 'all')

    if staff_filter == 'yes':
        users = users.filter(is_staff=True)
    elif staff_filter == 'no':
        users = users.filter(is_staff=False)

    if super_filter == 'yes':
        users = users.filter(is_superuser=True)
    elif super_filter == 'no':
        users = users.filter(is_superuser=False)

    if active_filter == 'yes':
        users = users.filter(is_active=True)
    elif active_filter == 'no':
        users = users.filter(is_active=False)

    return render(request, 'view_users.html', {
        'users': users,
        'staff_filter': staff_filter,
        'super_filter': super_filter,
        'active_filter': active_filter
    })


@staff_member_required(login_url='admin_login')
def edit_user(request, user_id):
    """Admin can update an existing user."""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username').strip()
        user.email = request.POST.get('email').strip()
        user.first_name = request.POST.get('first_name').strip()
        user.last_name = request.POST.get('last_name').strip()
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'

        password = request.POST.get('password').strip()
        if password:
            user.set_password(password)
            if user == request.user:
                update_session_auth_hash(request, user)  # keeps admin logged in

        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('admin_dashboard')  # Redirect to dashboard instead of view_users

    return render(request, 'edit_user.html', {'user': user})


@staff_member_required(login_url='admin_login')
def delete_user(request, user_id):
    """Admin can delete a user."""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('view_users')

    return render(request, 'delete_user.html', {'user': user})


@staff_member_required(login_url='admin_login')
def admin_logout(request):
    """
    Logs out the currently logged-in admin and redirects to the admin login page.
    """
    logout(request)
    messages.info(request, 'Admin logged out successfully.')
    return redirect('admin_login')

def verify_user(request, user_id, user_type):
    if request.method == 'POST':
        if user_type == 'owner':
            user = get_object_or_404(Owner, id=user_id)
        else:
            user = get_object_or_404(Renter, id=user_id)
        user.is_verified = True
        user.save()
    return redirect('admin_dashboard')

def reject_user(request, user_id, user_type):
    if request.method == 'POST':
        if user_type == 'owner':
            user = get_object_or_404(Owner, id=user_id)
        else:
            user = get_object_or_404(Renter, id=user_id)
        user.is_verified = False
        user.save()
    return redirect('admin_dashboard')

@login_required
def post_new_listing(request):
    # Only owners can post
    profile = Profile.objects.filter(user=request.user).first()
    if not profile or profile.role != 'owner':
        messages.error(request, "Access denied.")
        return redirect('home')

    if request.method == 'POST':
        room_title = request.POST.get('room_title')
        location = request.POST.get('location')
        rent = request.POST.get('rent')
        room_size = request.POST.get('room_size')
        occupancy = request.POST.get('occupancy')
        description = request.POST.get('description')
        image = request.FILES.get('images')  # matches your form input name "images"

        # Basic validation (you can extend)
        if not room_title or not location or not rent:
            messages.error(request, 'Please fill required fields.')
            return redirect('post_new_listing')

        Listing.objects.create(
            owner=request.user,
            room_title=room_title,
            location=location,
            rent=rent,
            room_size=room_size or 0,
            occupancy=occupancy or 0,
            description=description or '',
            image=image
        )

        messages.success(request, 'Listing posted successfully.')
        return redirect('renter_dashboard')

    return render(request, 'post_new_listing.html')


@login_required
def renter_dashboard(request):
    # Only renters allowed here per your flow — if you want everyone to see, remove role check
    profile = Profile.objects.filter(user=request.user).first()
    if not profile or profile.role != 'renter':
        messages.error(request, 'Access denied.')
        return redirect('home')

    listings = Listing.objects.all().order_by('-created_at')  # newest first
    return render(request, 'renter_dashboard.html', {'listings': listings})


@login_required
def view_details(request, room_id):
    room = get_object_or_404(Listing, id=room_id)

    if request.method == 'POST':
        BookingRequest.objects.create(
            renter=request.user,
            owner=room.owner,
            listing=room
        )
        messages.success(request, 'Booking request sent to the owner!')
        return redirect('renter_dashboard')

    return render(request, 'view_details.html', {'room': room})

def renter_profile(request):
    return render(request, 'renter_profile.html')

def owner_profile(request):
    return render(request, 'owner_profile.html')

@login_required
def notifications(request):
    profile = Profile.objects.filter(user=request.user).first()

    if profile.role == 'owner':
        notifications = BookingRequest.objects.filter(owner=request.user, status='pending')
    else:
        notifications = BookingRequest.objects.filter(renter=request.user).exclude(status='pending')

    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def respond_request(request, request_id, action):
    booking = get_object_or_404(BookingRequest, id=request_id)

    if request.user != booking.owner:
        messages.error(request, "Unauthorized action.")
        return redirect('notifications')

    if action == 'accept':
        booking.status = 'accepted'
    else:
        booking.status = 'rejected'

    booking.save()
    messages.success(request, f'Booking request {action}ed.')

    return redirect('notifications')


from django.views.decorators.http import require_POST

@require_POST
@login_required
def booking_accept(request, req_id):
    booking = get_object_or_404(BookingRequest, id=req_id, owner=request.user)
    booking.status = 'accepted'
    booking.save()
    # Optionally send notification back to renter
    return redirect('owner_dashboard')


@require_POST
@login_required
def booking_reject(request, req_id):
    booking = get_object_or_404(BookingRequest, id=req_id, owner=request.user)
    booking.status = 'rejected'
    booking.save()
    # Optionally send notification back to renter
    return redirect('owner_dashboard')

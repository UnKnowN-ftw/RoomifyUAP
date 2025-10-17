from django.urls import path
from . import views

urlpatterns = [
    # Main page
    path('', views.home, name='home'),

    # Login routes (role can be 'renter' or 'owner')
    path('login/<str:role>/', views.login_user, name='login_user'),

    # Register routes (role can be 'renter' or 'owner')
    path('register/<str:role>/', views.register_user, name='register_user'),

    # Logout route
    path('logout/', views.logout_user, name='logout_user'),

    # Dashboards
    path('dashboard/renter/', views.renter_dashboard, name='renter_dashboard'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),

    path('post-new-listing/', views.post_new_listing, name='post_new_listing'),

    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('verify/<int:user_id>/<str:user_type>/', views.verify_user, name='verify_user'),
    path('reject/<int:user_id>/<str:user_type>/', views.reject_user, name='reject_user'),


]
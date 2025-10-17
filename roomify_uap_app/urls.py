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
    path('dashboard/renter/profile/', views.renter_profile, name='renter_profile'),

    
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('post-new-listing/', views.post_new_listing, name='post_new_listing'),

    path('dashboard/admin/login/', views.admin_login, name='admin_login'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/users/', views.view_users, name='view_users'),
    path('dashboard/admin/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('verify/<int:user_id>/<str:user_type>/', views.verify_user, name='verify_user'),
    path('reject/<int:user_id>/<str:user_type>/', views.reject_user, name='reject_user'),
    path('dashboard/admin/logout/', views.admin_logout, name='admin_logout'),

    path('room/<int:room_id>/', views.view_details, name='view_details'),

]
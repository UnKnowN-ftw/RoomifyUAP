from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/<str:role>/', views.login_user, name='login_user'),
    path('register/<str:role>/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),


    path('dashboard/renter/', views.renter_dashboard, name='renter_dashboard'),
    path('dashboard/renter/profile/', views.renter_profile, name='renter_profile'),


    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/listings/', views.owner_listings, name='owner_listings'),
    path('owner/analytics/', views.owner_analytics, name='owner_analytics'),
    path('owner/messages/', views.owner_messages, name='owner_messages'),
    path('send-message/<int:listing_id>/', views.send_message, name='send_message'),
    path('dashboard/owner/profile/', views.owner_profile, name='owner_profile'),
    path('post-new-listing/', views.post_new_listing, name='post_new_listing'),
    path('owner/listing/edit/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('owner/listing/view/<int:listing_id>/', views.view_listing, name='view_listing'),
    path('listing/<int:listing_id>/delete/', views.delete_listing, name='delete_listing'),


    path('dashboard/admin/login/', views.admin_login, name='admin_login'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/users/', views.view_users, name='view_users'),
    path('dashboard/admin/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('verify/<int:user_id>/<str:user_type>/', views.verify_user, name='verify_user'),
    path('reject/<int:user_id>/<str:user_type>/', views.reject_user, name='reject_user'),
    path('dashboard/admin/logout/', views.admin_logout, name='admin_logout'),


    path('room/<int:room_id>/', views.view_details, name='view_details'),


    path('notifications/', views.notifications, name='notifications'),
    path('notifications/respond/<int:request_id>/<str:action>/', views.respond_request, name='respond_request'),
    path('clear-notifications/', views.clear_notifications, name='clear_notifications'),


    path('booking/accept/<int:req_id>/', views.booking_accept, name='booking_accept'),
    path('booking/reject/<int:req_id>/', views.booking_reject, name='booking_reject'),
]
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_ROLES = (
        ('owner', 'Owner'),
        ('renter', 'Renter'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
class Owner(models.Model):
    name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

class Renter(models.Model):
    name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    room_title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    room_size = models.IntegerField()
    occupancy = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_title

class BookingRequest(models.Model):
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.renter.username} -> {self.owner.username} ({self.status})"


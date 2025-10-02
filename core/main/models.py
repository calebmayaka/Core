# Django imports for database models and user authentication
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    
    This model customizes the default Django user to use email as the primary
    login field instead of username, and adds additional required fields.
    You can add extra fields here if needed (e.g., phone, organization).
    """
    # Email field that must be unique across all users
    email = models.EmailField(unique=True)
    
    # Phone number field - required for all users
    phone = models.CharField(max_length=15, blank=False, null=False)
    

    # Configuration: Use email instead of username for authentication
    USERNAME_FIELD = 'email'          # Primary login field
    REQUIRED_FIELDS = ['username']    # Fields required when creating superuser (username kept as backup)

    def __str__(self):
        """String representation of the user - returns email if available, otherwise username"""
        return self.email or self.username


class Customer(models.Model):
    """
    Customer profile model that extends user information for business purposes.
    
    This model creates a one-to-one relationship with CustomUser to store
    customer-specific information like business name and customer code.
    """
    # One-to-one relationship with CustomUser - each user can have one customer profile
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer_profile")
    
    # Customer's business or display name
    name = models.CharField(max_length=100)
    
    # Unique customer code for business identification/reference
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        """String representation showing customer name and code"""
        return f"{self.name} ({self.code})"


class Order(models.Model):
    """
    Order model representing customer purchases/transactions.
    
    Each order is linked to a customer and contains item details,
    amount, and timestamp information.
    """
    # Foreign key to Customer - each order belongs to one customer
    # CASCADE: if customer is deleted, all their orders are deleted too
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    
    # Description of the item/service ordered
    item = models.CharField(max_length=100)
    
    # Order amount with up to 10 digits total, 2 decimal places (e.g., 99999999.99)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamp of when the order was created (automatically set to current time)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """String representation showing order ID, item, and amount"""
        return f"Order {self.id} - {self.item} (${self.amount})"

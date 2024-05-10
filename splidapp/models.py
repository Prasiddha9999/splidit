from django.db import models
from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)  
#     username = models.CharField(max_length=100, unique=True)
    
#     from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Your custom fields here
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  
    username = models.CharField(max_length=100, unique=True)

    # Example for groups field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Unique related_name for groups
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )

    # Example for user_permissions field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Unique related_name for user_permissions
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_of_groups')
    invitation_link = models.CharField(max_length=100) 

class GroupMembers(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_members')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    is_admin = models.BooleanField(default=False)

class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

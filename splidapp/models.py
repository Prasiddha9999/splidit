from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_of_groups')
    invitation_link = models.CharField(max_length=100) 

    def __str__(self):
        return self.group_name

class GroupMembers(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_members')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    is_admin = models.BooleanField(default=False)


class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    expense_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_for = models.ManyToManyField(User, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)


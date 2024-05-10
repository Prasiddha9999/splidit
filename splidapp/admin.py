from django.contrib import admin
from .models import User, Group, GroupMembers, Expense

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email')  

# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')  

# class GroupMembersAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'group')  

# class ExpenseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'amount', 'date') 

admin.site.register(User)  
admin.site.register(Group)  
admin.site.register(GroupMembers)  
admin.site.register(Expense)  

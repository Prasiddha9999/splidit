from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import random
from .models import *

def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Login success")
            group_member = GroupMembers.objects.filter(user_id=user).first()
            last = Group.objects.filter(group_name = group_member.group_id).first()
            
        
            if last is not None:
                return redirect(reverse('homeview', args=[last.group_id]))
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid Login Credentials')

    return redirect('index')

def register_view(request):
    print("Hello love ")
    if request.method == 'POST':
        username = request.POST.get('new_username')
        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('index')  
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('index')  

        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Passwords do not match')

    return redirect('index')  

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

from django.urls import reverse

@login_required
def home(request):
    if request.method == 'POST':
        group_name = request.POST.get('groupname')
        user = request.user
        invitation_link = ''.join(random.choices('0123456789', k=9))
        new_group = Group.objects.create(group_name=group_name, invitation_link=invitation_link, admin_id=user)
        GroupMembers.objects.create(group_id=new_group, user_id=user, is_admin=True)  
        messages.success(request, 'Group created successfully!')
        
        # Redirect to homeview by passing group_id as a positional argument
        return redirect(reverse('homeview', args=[new_group.pk]))
        
    elif request.method == 'GET':
        group_link = request.GET.get('joingroup')
        user = request.user
        group = Group.objects.filter(invitation_link=group_link).first()
        if group:
            GroupMembers.objects.create(group_id=group, user_id=user)
            return redirect(reverse('homeview', args=[group.pk]))
    return render(request, "home.html")





 

@login_required
def homeview(request, groupid):
    try:
        group = Group.objects.get(pk=groupid)
        return render(request, "homeview.html", {'group': group})
    except Group.DoesNotExist:
        messages.error(request, 'Group matching query does not exist.')

        return redirect('home')
    
    
        


@login_required
def expenselist(request, group_id):
    lst = Expense.objects.filter(group_id=group_id)
    group = Group.objects.filter(group_id=group_id).first()
    print(lst)
    return render(request, "expenselist.html",{'lst':lst, 'group':group})

@login_required
def addexpense(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    groupname = Group.objects.filter(group_id=group_id).first()

    if request.method == 'POST':
        about = request.POST.get('about')
        expense_by_id = request.POST.get('expenseby')
        expense_for_ids = request.POST.getlist('expensefor')
        amount = request.POST.get('amount')

        # Create the expense record
        try:
            expense_by = User.objects.get(pk=expense_by_id)
            expense_for_users = group.group_members.all()
            expense = Expense.objects.create(
                group_id=group,  # Provide the group_id
                description=about,
                expense_by=expense_by,
                amount=amount,
            )
            expense.expense_for.add(*expense_for_users)

            messages.success(request, 'Expense created successfully!')
        except Exception as e:
            messages.error(request, f'Failed to create expense: {str(e)}')

        return redirect('expenselist', group_id=group_id)

    # Filter users based on group members
    users = group.group_members.values_list('user_id', flat=True)
    user = User.objects.filter(pk__in=users)
    print(user)

    return render(request, "addexpense.html", {'user': user, 'groupname': groupname})







@login_required
def editexpense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)

    if request.method == 'POST':
        try:
            about = request.POST.get('about')
            print(about)
            expense_by_id = request.POST.get('expenseby')
            expense_for_ids = request.POST.getlist('expensefor')
            amount = request.POST.get('amount')
            expense_by = User.objects.get(pk=expense_by_id)
            expense_for_users = User.objects.filter(pk__in=expense_for_ids)
            expense.description = about
            expense.expense_by = expense_by
            expense.amount = amount
            expense.save()
            expense.expense_for.set(expense_for_users)
            
            messages.success(request, 'Expense updated successfully!')
            return redirect('expenselist', group_id=expense.group_id_id)
        except Exception as e:
            messages.error(request, f'Failed to update expense: {str(e)}')
    users = expense.group_id.group_members.all()
    expense_for_ids = list(expense.expense_for.values_list('id', flat=True))  
    return render(request, "editexpense.html", {'expense': expense, 'users': users, 'expense_for_ids': expense_for_ids})





@login_required
def settle(request):
    return render(request, "settle.html")

@login_required
def grouplist(request):
    user = request.user
    group_memberships = GroupMembers.objects.filter(user_id=user)
    return render(request, "grouplist.html", {'groups': group_memberships})


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        group.delete()
        GroupMembers.objects.filter(group_id=group_id).delete()
        return redirect('grouplist')
    return redirect('home')


@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    GroupMembers.objects.filter(group_id=group, user_id=request.user).delete()
    return redirect('grouplist')
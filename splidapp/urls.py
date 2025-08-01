from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('settle/', views.settle, name='settle'),
    path('homeview/<int:groupid>/', views.homeview, name='homeview'),
    path('expenselist/<int:group_id>/', views.expenselist, name='expenselist'),
    path('addexpense/<int:group_id>/', views.addexpense, name='addexpense'),
    path('editexpense/<int:expense_id>/', views.editexpense, name='editexpense'),
    path('grouplist/', views.grouplist, name='grouplist'),
    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),
    path('leave_group/<int:group_id>/', views.leave_group, name='leave_group')
    
    
]
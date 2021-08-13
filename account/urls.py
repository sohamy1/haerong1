from django.contrib import admin
from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('myaccount/', views.myaccount_view, name="myaccount"),
    path('account_edit/', views.edit_view, name="account_edit"),
    path('account_delete/', views.deleted_view, name="account_delete"),
    path('register/', views.register_view, name="register"),
    path('finder/', views.finder_view, name="finder"),
    path('finder_verify/', views.finder_verify_view, name="finder_verify"),
    path('account_info/<id>', views.account_info, name="account_info"),
]

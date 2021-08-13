from django.shortcuts import render, redirect
from board.models import Posts
from account.models import CustomUser
from django.core.paginator import Paginator  

def home_view(request):
    new_posts = Posts.objects.order_by('-created_at')[:9]
    hot_posts = Posts.objects.order_by('-stars')[:12]
    top_users = CustomUser.objects.order_by('-score')[:9]
    
    return render(request, "home.html", {'new_posts':new_posts, 'hot_posts':hot_posts, 'top_users':top_users})

def test_view(request):
    new_posts = Posts.objects.order_by('-created_at')[:9]
    hot_posts = Posts.objects.order_by('-stars')[:12]
    top_users = CustomUser.objects.order_by('-score')[:9]
    
    return render(request, "test.html", {'new_posts':new_posts, 'hot_posts':hot_posts, 'top_users':top_users})
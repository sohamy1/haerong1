from django.contrib import admin
from django.urls import path
from comment import views

app_name = "comment"

urlpatterns = [
    path('comment/ <id>', views.comment_view, name="comment"),
    path('comment_like/ <id>', views.comment_stars_view, name="comment_like"),
    path('comment_del/ <id>', views.comment_del_view, name="comment_del"),
]

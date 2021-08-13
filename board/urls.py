from django.contrib import admin
from django.urls import path
from board import views

app_name = "board"

urlpatterns = [
    path('write/', views.write_view, name="write"),
    path('detail/<id>', views.detail_view, name="detail"),
    path('detail_next/<id>', views.detail_next, name="detail_next"),
    path('detail_previous/ <id>', views.detail_back, name="detail_back"),
    path('edit/ <id>', views.edit_view, name="edit"),
    path('stars/ <id>', views.stars_view, name="stars"),
    path('delete/ <id>', views.delete_view, name="delete"),

    path('board_all', views.board_all, name="board_all"),
    path('board_hot', views.board_hot, name="board_hot"),

    path('board_amphibian', views.board_amphibian, name="board_amphibian"),
    path('board_bird', views.board_bird, name="board_bird"),
    path('board_etc', views.board_etc, name="board_etc"),
    path('board_fish', views.board_fish, name="board_fish"),
    path('board_mammals', views.board_mammals, name="board_mammals"),
    path('board_reptilia', views.board_reptilia, name="board_reptilia"),

    path('search', views.search_view, name="search")
]

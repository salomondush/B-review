
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("new_post", views.new_post, name="new_post"),
    path("<int:user_id>/profile", views.profile, name="profile")
]

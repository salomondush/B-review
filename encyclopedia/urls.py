from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.title, name="title"),
    path("wiki/new-entry", views.newentry, name="newentry"),
    path("wiki/search", views.search, name="search"),
    path("wiki/edit/<str:entry_title>/", views.edit, name="edit"),
    path("wiki/random_entry", views.random_entry, name="random_entry")
]

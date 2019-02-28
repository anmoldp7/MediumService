from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name = "home_page"),
    path("tag/<str:pk>", views.tag_page, name = "tag_page"),
    path("search", views.search_history, name = "search_history"),
]
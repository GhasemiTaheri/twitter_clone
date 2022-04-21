from django.urls import path

from . import views

urlpatterns = [
    path("", views.load_post, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    # path("load_post/<str:type>", views.load_post, name="load_post"),
    path("following-post", views.load_post, name="following_post"),
    path("user/<str:username>", views.profile_view, name="profile_view"),
]

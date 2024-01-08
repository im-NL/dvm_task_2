from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("", views.index),
    path("check", views.check),
    path("login/", views.login),
    path("logout", LogoutView.as_view()),
    # path("register/", views.register),
    # path("profile/", views.profile),

]
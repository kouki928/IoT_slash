from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="auth"),
    path("login", views.login, name="")
]

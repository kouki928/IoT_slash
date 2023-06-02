from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="auth"),
    path("signUp", views.signUp, name="signUp"),
    path("mypage", views.mypage, name="mypage"),
]

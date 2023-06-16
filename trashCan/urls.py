from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="auth"),
    path("signUp", views.signUp, name="signUp"),
    path("mypage", views.mypage, name="mypage"),
    path("send_email", views.send_email, name="sendEmail"),
    path("notice", views.notice, name="notice"),
    path("points", views.points, name="points"),
]

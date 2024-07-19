from django.urls import re_path

from testovac.login.views import login, logout, register

urlpatterns = [
    re_path(r"^login/$", login, name="login"),
    re_path(r"^logout/$", logout, name="logout"),
    re_path(r"^register/$", register, name="registration"),
]

from django.urls import re_path

from testovac.achievements import views

urlpatterns = [
    re_path(r"^$", views.overview, name="achievement_overview"),
    re_path(r"^(?P<slug>[A-Za-z0-9_-]+)/$", views.detail, name="achievement_detail"),
]

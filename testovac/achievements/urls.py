from django.conf.urls import url

from testovac.achievements import views

urlpatterns = [
    url(r'^$', views.overview, name="achievement_overview"),
    url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', views.detail, name="achievement_detail"),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('oauth/', views.oauth, name='slack_oauth'),
    path('events/', views.Events.as_view(), name='events0'),
]

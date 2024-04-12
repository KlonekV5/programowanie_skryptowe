from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('answers', views.answers, name='answers'),
    path('poll', views.poll, name='poll'),
    path('save', views.save, name='save'),
]

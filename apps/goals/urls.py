from django.urls import path

from apps.goals import views

urlpatterns = [
    path('', views.goals, name='goal_list'),
]
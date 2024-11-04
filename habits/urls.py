from django.urls import path
from .views import (
    HabitListView,
    HabitDetailView,
    PublicHabitListView
)

urlpatterns = [
    path('habits/', HabitListView.as_view(), name='habit-list'),
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
    path('habits/public/', PublicHabitListView.as_view(), name='public-habit-list'),
]
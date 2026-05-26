from django.urls import path
from habits.views import (
    HabitListView,
    HabitPublicListView,
    HabitCreateView,
    HabitDetailView,
)

urlpatterns = [
    path("", HabitListView.as_view(), name="habit-list"),
    path("public/", HabitPublicListView.as_view(), name="habit-public-list"),
    path("create/", HabitCreateView.as_view(), name="habit-create"),
    path("<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
]
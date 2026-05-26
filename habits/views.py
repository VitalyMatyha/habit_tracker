from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.paginators import HabitPaginator


class HabitListView(ListAPIView):
    """Список привычек текущего пользователя."""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitPublicListView(ListAPIView):
    """Список публичных привычек."""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitCreateView(CreateAPIView):
    """Создание привычки."""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(RetrieveUpdateDestroyAPIView):
    """Просмотр, редактирование, удаление привычки."""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
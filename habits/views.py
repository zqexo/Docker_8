from django.core.exceptions import ValidationError
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from habits.models import Habit
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Habit с дополнительными эндпоинтами для публичных и пользовательских привычек.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        if self.action == "public_habits":
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Проверяем условия перед сохранением привычки
        if serializer.validated_data.get("reward") and serializer.validated_data.get(
            "related_habit"
        ):
            raise ValidationError(
                "Нельзя одновременно указать вознаграждение и связанную привычку."
            )
        if serializer.validated_data.get("completion_time") > 120:
            raise ValidationError(
                "Время на выполнение привычки не должно превышать 120 секунд."
            )
        if (
            serializer.validated_data.get("related_habit")
            and not serializer.validated_data["related_habit"].is_pleasant
        ):
            raise ValidationError(
                "Связанная привычка должна быть отмечена как приятная."
            )
        if serializer.validated_data.get("is_pleasant") and (
            serializer.validated_data.get("reward")
            or serializer.validated_data.get("related_habit")
        ):
            raise ValidationError(
                "Приятная привычка не может иметь вознаграждения или связанную привычку."
            )
        if serializer.validated_data.get("frequency") not in ["daily", "weekly"]:
            raise ValidationError(
                "Привычку нельзя выполнять реже одного раза в неделю."
            )

        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def public_habits(self, request):
        """
        Эндпоинт для списка публичных привычек.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def my_habits(self, request):
        """
        Эндпоинт для списка привычек текущего пользователя.
        """
        queryset = Habit.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

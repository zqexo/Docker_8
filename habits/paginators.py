from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    page_size = 5  # Количество элементов на странице
    page_size_query_param = "page_size"
    max_page_size = (
        10  # Максимальное количество элементов на странице, если указано через запрос
    )

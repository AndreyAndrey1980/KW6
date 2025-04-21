from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    # Количество объектов на одной странице по умолчанию
    page_size = 5

    # Позволяет клиенту указывать желаемое количество объектов на странице через параметр `page_size`
    page_size_query_param = 'page_size'

    # Максимальное количество объектов на странице, даже если клиент укажет большее значение
    max_page_size = 100

    # Сортировка по умолчанию (заметь: параметр `ordering` здесь не влияет напрямую — он используется в фильтрации)
    ordering = "id"  # Этот атрибут не обрабатывается пагинатором напрямую — если нужен порядок, лучше использовать OrderingFilter

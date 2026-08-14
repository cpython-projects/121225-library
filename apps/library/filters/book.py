import django_filters

from apps.library.models import Category, Post, Book
from apps.library.serializers import CategorySerializer, PostSerializer, BookSerializer


class BookFilter(django_filters.FilterSet):
    overdue = django_filters.BooleanFilter(method='filter_overdue')
    class Meta:
        model = Book
        fields = ['category', 'libraries']

    def filter_overdue(self, queryset, name, value):
        if value:
            return queryset.filter(overdue=True)
from django.db.models import Count
from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view

from apps.library.models import Category, Post, Book, Author
from apps.library.serializers import CategorySerializer, PostSerializer, BookSerializer, AuthorSerializer
from apps.library.filters import BookFilter


@api_view(['POST'])
@transaction.atomic
def create_author_with_book(request):
    author = Author.objects.create(
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        date_of_birth=request.data['date_of_birth'],
        rating=request.data['rating']
    )
    book = Book.objects.create(
        title=request.data['title'],
        author=author,
        published_at=request.data['published_at'],
        genre=request.data['genre'],
    )

    return Response(data={'message': 'Author created'}, status=status.HTTP_201_CREATED)



class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def perform_create(self, serializer):
        with transaction.atomic():
            pass

    @action(detail=False, methods=['GET'])
    def statistics(self, request):
        categories = Category.objects.annotate(book_count=Count('books'))
        data = [
            {
                'id': category.id,
                'name': category.name,
                'count': category.book_count
            }
            for category in categories
        ]
        return Response(data, status=status.HTTP_200_OK)



class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # # filterset_fields = ['genre', 'category', 'publisher']
    # filterset_class = BookFilter
    # search_fields = ['title', 'author__first_name', 'author__last_name']
    # ordering_fields = ['published_at', 'page_count', 'genre']

    serializer_classes = {
        'list': PostSerializer,
        'retrieve': PostSerializer,
        'update': PostSerializer,
        'create': PostSerializer,
        'destroy': PostSerializer,
        'partial_update': PostSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, PostSerializer)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         pass
    #     if self.action == 'create':
    #         pass


    @action(detail=False, methods=['GET'])
    def genre_statistics(self, request):
        data = Book.objects.values('genre').annotate(count=Count('id')).order_by('-count')
        return Response(list(data), status=status.HTTP_200_OK)















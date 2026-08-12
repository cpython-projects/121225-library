from datetime import timedelta

from django.db.models import Avg
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apps.library.models import Post, Category
from apps.library.serializers import PostSerializer
from rest_framework import mixins

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


from .serializers import (AuthorSerializer,
                          AuthorDetailSerializer, BookSerializer,
                          BookCreateSerializer,
                        CategorySerializer,
                          )
from .models import Author, AuthorDetail, Book

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    lookup_field = 'name'
    lookup_url_kwarg = 'cat_name'











class BookListGenericAPIView(ListCreateAPIView):
    queryset = Book.objects.select_related('author', 'category').all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ['genre', 'category', 'publisher']
    search_fields = ['title', 'author__first_name', 'author__last_name']
    ordering_fields = ['published_at', 'page_count', 'genre']





    # def get_queryset(self):
    #     all_avg = Book.objects.aggregate(avg_rating=Avg('reviews__rating'))['avg_rating']
    #     return Book.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gt=all_avg)
    #
    # def perform_create(self, serializer):
    #     if not serializer.validated_data['category']:
    #         default_category, _ = Category.objects.get_or_create(name='Uncategorized')
    #         serializer.save(category=default_category)
    #     else:
    #         serializer.save()


class BookDetailGenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related('author', 'category').all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.select_related('author', 'category').filter(is_banned=False)

    # def get_object(self):
    #     book = get_object_or_404(
    #         self.filter_queryset(self.get_queryset()),
    #         pk=self.kwargs['pk'], is_banned=False
    #     )
    #     self.check_object_permissions(self.request, book)
    #     return book


    def retrieve(self, request, *args, **kwargs):
        # response = super().retrieve(request, *args, **kwargs)
        #
        # # Добавление поля к ответу, проверяющего, что цена со скидкой меньше цены
        # if response.data.get('discounted_price') is not None and response.data.get('price') is not None:
        #     response.data['is_discounted'] = response.data['discounted_price'] < response.data['price']
        # else:
        #     response.data['is_discounted'] = False
        # return response
        # response = super().retrieve(request, *args, **kwargs)
        # instance = self.get_object()
        # response.data['is_new'] = instance.published_at > timezone.now().date() - timedelta(days=360)
        # return response

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['is_new'] = instance.published_at > timezone.now().date() - timedelta(days=360)
        return Response(data)










# class BookListGenericAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
#     queryset = Book.objects.select_related('author', 'category').all()
#     serializer_class = BookSerializer
#
#     def get_queryset(self):
#         queryset = Book.objects.select_related('author', 'category')
#         author_id = self.request.query_params.get('author')
#         genre = self.request.query_params.get('genre')
#         if author_id:
#             queryset = queryset.filter(author__id=author_id)
#         if genre:
#             queryset = queryset.filter(genre=genre)
#         return queryset
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return BookSerializer
#         if self.request.method == 'POST':
#             return BookCreateSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class BookDetailGenericAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,  GenericAPIView):
#     queryset = Book.objects.select_related('author', 'category').all()
#     serializer_class = BookSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#





# class BookListGenericAPIView(GenericAPIView):
#     queryset = Book.objects.select_related('author', 'category').all()
#     serializer_class = BookSerializer
#
#     def get_queryset(self):
#         queryset = Book.objects.select_related('author', 'category')
#         author_id = self.request.query_params.get('author')
#         genre = self.request.query_params.get('genre')
#         if author_id:
#             queryset = queryset.filter(author__id=author_id)
#         if genre:
#             queryset = queryset.filter(genre=genre)
#         return queryset
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return BookSerializer
#         if self.request.method == 'POST':
#             return BookCreateSerializer
#
#     def get(self, request, *args, **kwargs):
#         books = self.get_queryset()
#         serializer = self.get_serializer(books, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class BookDetailGenericAPIView(GenericAPIView):
#     queryset = Book.objects.select_related('author', 'category').all()
#     serializer_class = BookSerializer
#
#     def get(self, request, *args, **kwargs):
#         book = self.get_object()
#         serializer = self.get_serializer(book)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         book = self.get_object()
#         serializer = self.get_serializer(book, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def patch(self, request, *args, **kwargs):
#         book = self.get_object()
#         serializer = self.get_serializer(book, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def delete(self, request, *args, **kwargs):
#         book = self.get_object()
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class AuthorListAPIView(APIView):
#     def get(self, request):
#         authors = Author.objects.filter(deleted_at__isnull=True).select_related('details')
#         serializer = AuthorSerializer(authors, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = AuthorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class AuthorDetailAPIView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Author, pk=pk, deleted_at__isnull=True)
#
#     def get(self, request, pk):
#         author = self.get_object(pk)
#         serializer = AuthorSerializer(author, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         author = self.get_object(pk)
#         serializer = AuthorSerializer(author, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk):
#         author = self.get_object(pk)
#         author.deleted_at = timezone.now()
#         author.save(update_fields=['deleted_at'])
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#
# class BookListAPIView(APIView):
#     def get(self, request):
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = BookSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class BookDetailAPIView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Book, pk=pk)
#
#     def get(self, request, pk):
#         book = self.get_object(pk)
#         serializer = AuthorSerializer(book, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class PostListAPIView(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#
# class PostDetailView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Post, pk=pk)
#
#     def get(self, request, pk, *args, **kwargs):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk, *args, **kwargs):
#         post = self.get_object(pk)
#         # partial не передан → False. Отсутствующие в теле запроса поля
#         # с default на уровне модели будут молча заменены на этот default.
#         serializer = PostSerializer(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def patch(self, request, pk, *args, **kwargs):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
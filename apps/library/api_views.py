from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.generics import get_object_or_404

from .models import Book
from .serializers import BookListSerializer, BookCreateSerializer
from .pagination import BookPagination


@api_view(['GET', 'POST'])
def books_list_create(request):
    if request.method == 'GET':
        books = Book.objects.select_related('author', 'category').all()
        books_serializer = BookListSerializer(books, many=True)
        return Response(books_serializer.data, status=status.HTTP_200_OK)

    serializer = BookCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def books_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'GET':
        serializer = BookListSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = BookCreateSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        serializer = BookCreateSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView


# class BookListCreateAPIView(APIView):
#     def get(self, request):
#         books = Book.objects.select_related('author', 'category').all()
#         books_serializer = BookListSerializer(books, many=True)
#         return Response(books_serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = BookCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    def get(self, request, pk):
        x = 5 / 0
        book = get_object_or_404(Book, pk=pk)
        serializer = BookListSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookCreateSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookCreateSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListCreateAPIView(APIView):

    ALLOW_SORT_FIELDS = ('title', 'published_at', 'page_count')

    def get(self, request):
        # filters = {}
        #
        # author_last_name = request.query_params.get('author')
        # if author_last_name:
        #     filters['author__last_name__icontains'] = author_last_name
        # books = Book.objects.select_related('author', 'category').filter(**filters)


        books = Book.objects.select_related('author', 'category').all()

        author_last_name = request.query_params.get('author')
        if author_last_name:
            books = books.filter(author__last_name__icontains=author_last_name)
        category = request.query_params.get('category')
        if category:
            books = books.filter(category__icontains=category)
        genre = request.query_params.get('genre')
        if genre:
            books = books.filter(genre__icontains=genre)


        sort_by = request.query_params.get('sort_by', 'published_at').strip().lower()
        sort_order = request.query_params.get('sort_order', 'desc')

        if sort_by in self.ALLOW_SORT_FIELDS:
            if sort_order == 'desc':
                sort_by = f'-{sort_by}'

            books = books.order_by(sort_by)

        paginator = BookPagination()
        page = paginator.paginate_queryset(books, request)

        books_serializer = BookListSerializer(page, many=True)
        return Response(books_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        pass

























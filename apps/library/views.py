from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .serializers import AuthorSerializer, AuthorDetailSerializer, BookSerializer
from .models import Author, AuthorDetail, Book


class AuthorListAPIView(APIView):
    def get(self, request):
        authors = Author.objects.filter(deleted_at__isnull=True).select_related('details')
        serializer = AuthorSerializer(authors, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthorDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Author, pk=pk, deleted_at__isnull=True)

    def get(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        author = self.get_object(pk)
        author.deleted_at = timezone.now()
        author.save(update_fields=['deleted_at'])
        return Response(status=status.HTTP_204_NO_CONTENT)



class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = AuthorSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
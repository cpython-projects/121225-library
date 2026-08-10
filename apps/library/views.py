from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .serializers import AuthorSerializer, AuthorDetailSerializer
from .models import Author, AuthorDetail



class AuthorListAPIView(APIView):
    def get(self, request):
        authors = Author.objects.filter(deleted_at__isnull=True).select_related('details')
        serializer = AuthorSerializer(authors, many=True)
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
        serializer = AuthorSerializer(author)
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
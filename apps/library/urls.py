from django.urls import path
from .views import AuthorListAPIView, AuthorDetailAPIView, BookListAPIView, BookDetailAPIView

app_name = 'library'

urlpatterns = [
    path('authors/', AuthorListAPIView.as_view(), name='authors-list'),
    path('authors/<uuid:pk>/', AuthorDetailAPIView.as_view(), name='author-detail'),
    path('books/', BookListAPIView.as_view(), name='books-list'),
    path('books/<uuid:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
]
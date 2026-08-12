from django.urls import path
# from .views import AuthorListAPIView, AuthorDetailAPIView, BookListAPIView, BookDetailAPIView, PostListAPIView, PostDetailView
from .views import BookListGenericAPIView, BookDetailGenericAPIView, CategoryListAPIView, CategoryDetailAPIView

app_name = 'library'

urlpatterns = [
    # path('authors/', AuthorListAPIView.as_view(), name='authors-list'),
    # path('authors/<uuid:pk>/', AuthorDetailAPIView.as_view(), name='author-detail'),

    path('books/', BookListGenericAPIView.as_view(), name='books-list'),
    path('books/<uuid:pk>/', BookDetailGenericAPIView.as_view(), name='book-detail'),

    path('categories/', CategoryListAPIView.as_view(), name='categories-list'),
    path('categories/<str:cat_name>/', CategoryDetailAPIView.as_view(), name='categories-detail'),


    # path('books/', BookListAPIView.as_view(), name='books-list'),
    # path('books/<uuid:pk>/', BookDetailAPIView.as_view(), name='book-detail'),

    # path('posts/', PostListAPIView.as_view(), name='posts-list'),
    # path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]